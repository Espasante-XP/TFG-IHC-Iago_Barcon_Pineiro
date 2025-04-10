#!/usr/bin/env python
# coding: utf-8


from cellpose import models, train, io
import json
from utils import obter_lista_ficheiros, es_extension_imagen_string, es_ruta_valida, es_num_positivo_string, es_numero, es_extension_mascara_string
from pathlib import Path
import numpy as np


model = models.Cellpose(gpu=True, model_type='cyto3')

cargar_datos_internamente = True

archivo_json = '../../config/training.json'


archivo_abierto = open(archivo_json)

nombre_dir_entrenamiento = 'path_entrenamiento'

nombre_dir_validacion = 'path_validacion'

nombre_ext_imagenes = 'extension_imagen'

nombre_ext_mascara = 'extension_mascara'

nombre_channels = 'channels'

nombre_normalize = 'normalize'

nombre_weight_decay = 'weight_decay'

nombre_learning_rate = 'learning_rate'

nombre_batch_size = 'batch_size'

nombre_epochs = 'num_epochs'

nombre_destino_reentrenamiento = 'destino_reentrenamiento'

nombre_guardar_cada = 'guardar_cada'

nombre_min_train_masks = 'min_train_masks'

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_dir_entrenamiento = valores_parametros_modelo[nombre_dir_entrenamiento]

if(Path(texto_valor_dir_entrenamiento).exists() and Path(texto_valor_dir_entrenamiento).is_dir()):
    root_training_directory = texto_valor_dir_entrenamiento 
else:
    print("Error, el valor introducido para el directorio de entrenamiento no es válido")
    exit()


texto_valor_dir_validacion = valores_parametros_modelo[nombre_dir_validacion]

if(Path(texto_valor_dir_validacion).exists() and Path(texto_valor_dir_validacion).is_dir()):
    root_validation_directory = texto_valor_dir_validacion 
else:
    print("Error, el valor introducido para el directorio de validación no es válido")
    exit()


texto_valor_ext_imagenes = valores_parametros_modelo[nombre_ext_imagenes]

if(es_extension_imagen_string(texto_valor_ext_imagenes)): 
    if(texto_valor_ext_imagenes.startswith('.')):
        ext_imagenes = texto_valor_ext_imagenes
    else:
        ext_imagenes = '.' + texto_valor_ext_imagenes    
else:
    print("Error, el valor introducido para la extensión de las imagenes no es válido")
    exit()


texto_valor_ext_mascara = valores_parametros_modelo[nombre_ext_mascara]

if(es_extension_mascara_string(texto_valor_ext_mascara)): 
    if(texto_valor_ext_mascara.startswith('.')):
        ext_mascara = texto_valor_ext_mascara
    else:
        ext_mascara = '.' + texto_valor_ext_mascara
    if(ext_mascara == ext_imagenes):
        print("Error, el valor introducido para la extensión de las máscaras y las imágenes es el mismo")
        exit()
    if(ext_mascara == '.npy'):
        print("Warning: Solo se pueden cargar las máscaras internamente si están en un formato de imágenes, se realizará carga local")
        cargar_datos_internamente = False  
else:
    print("Error, el valor introducido para la extensión de las máscaras no es válido")
    exit()


valor_channels = valores_parametros_modelo[nombre_channels]

if isinstance(valor_channels, list):
    # Comprobar si es una lista simple o una lista de listas
    if all(isinstance(item, list) for item in valor_channels):  # Si es una lista de listas
        for sublista in valor_channels:
            if not (isinstance(sublista, list) and len(sublista) == 2 and 
                    all(isinstance(x, (int, float)) and 0 <= x <= 3 for x in sublista)):
                print(f"Error, el valor introducido para la variable {nombre_channels} no es válido")
                exit()
        es_lista_de_listas = True
    else:  # Si es una lista simple
        if not (len(valor_channels) == 2 and 
                all(isinstance(x, (int, float)) and 0 <= x <= 3 for x in valor_channels)):
            print(f"Error, el valor introducido para la variable {nombre_channels} no es válido")
            exit()
    # Si pasa todas las validaciones, asignar el valor
    channels = valor_channels
    es_lista_de_listas = False
else:
    print(f"Error, el valor introducido para la variable {nombre_channels} no es una lista")
    exit()


texto_valor_normalize = valores_parametros_modelo[nombre_normalize]

if(texto_valor_normalize.isalpha() and texto_valor_normalize == "True"):
    normalize = True
elif (texto_valor_normalize.isalpha() and texto_valor_normalize == "False"):
    normalize = False
else:
    print(f"Error, el valor introducido para la variable {nombre_normalize} no es válido")
    exit()


texto_valor_weight_decay = valores_parametros_modelo[nombre_weight_decay]

if(es_numero(texto_valor_weight_decay)):
    if(float(texto_valor_weight_decay) <= 1 and float(texto_valor_weight_decay) >= 0):
        weight_decay = float(texto_valor_weight_decay)
    else:
        print(f"Error, el valor introducido para la variable {nombre_weight_decay} no es válido")
        exit()        
else:
    print(f"Error, el valor introducido para la variable {nombre_weight_decay} no es válido")
    exit()


texto_valor_learning_rate = valores_parametros_modelo[nombre_learning_rate]

if(es_num_positivo_string(texto_valor_learning_rate)):
    if(float(texto_valor_learning_rate) <= 1):
        learning_rate = float(texto_valor_learning_rate)
    else:
        print(f"Error, el valor introducido para la variable {nombre_learning_rate} no es válido")
        exit()    
else:
    print(f"Error, el valor introducido para la variable {nombre_learning_rate} no es válido")
    exit()


texto_valor_batch_size = valores_parametros_modelo[nombre_batch_size]

if(es_num_positivo_string(texto_valor_batch_size)):
    batch_size = int(texto_valor_batch_size)
else:
    print(f"Error, el valor introducido para la variable {nombre_batch_size} no es válido")
    exit()


texto_valor_num_epochs = valores_parametros_modelo[nombre_epochs]

if(es_num_positivo_string(texto_valor_num_epochs)):
    num_epochs = int(texto_valor_num_epochs)
else:
    print(f"Error, el valor introducido para la variable {nombre_epochs} no es válido")
    exit()


texto_valor_destino_reentrenamiento = valores_parametros_modelo[nombre_destino_reentrenamiento]

if(es_ruta_valida(texto_valor_destino_reentrenamiento)):
    destino_reentrenamiento = texto_valor_destino_reentrenamiento 
else:
    print("Error, el valor introducido para el directorio de salida no es válido")
    exit()


texto_valor_guardar_cada = valores_parametros_modelo[nombre_guardar_cada]

if(es_num_positivo_string(texto_valor_guardar_cada)):
    guardar_cada = int(texto_valor_guardar_cada)
    if(guardar_cada >= num_epochs):
        print(f"Warning: El valor de {nombre_guardar_cada} es igual o superior al de {nombre_epochs}")
else:
    print(f"Error, el valor introducido para la variable {nombre_guardar_cada} no es válido")
    exit()


texto_valor_min_train_masks = valores_parametros_modelo[nombre_min_train_masks]

if(es_numero(texto_valor_min_train_masks)):
    if(int(texto_valor_min_train_masks) >= 0):
        min_train_masks = int(texto_valor_min_train_masks)
    else:
        print(f"Error, el valor introducido para la variable {nombre_min_train_masks} no es válido")
        exit()   
else:
    print("Error, el valor introducido para la variable normalize no es válido")
    exit()


nombre_modelo = "modelo_reentrenado"

train_files = []

train_files = obter_lista_ficheiros(root_training_directory, ext_imagenes)

train_labels_files = []

train_labels_files = obter_lista_ficheiros(root_training_directory, ext_mascara)

test_files = []

test_files = obter_lista_ficheiros(root_validation_directory, ext_imagenes)

test_labels_files = []

test_labels_files = obter_lista_ficheiros(root_validation_directory, ext_mascara)

# Comprobación de que hay el mismo número de imágenes y máscaras tanto en entrenamiento como en validación
try:
    assert len(train_files) == len(train_labels_files), "El número de archivos de entrenamiento no coincide con el número de máscaras."

    assert len(test_files) == len(test_labels_files), "El número de archivos de validación no coincide con el número de máscaras."

    if(es_lista_de_listas):
        assert len(train_files) == len(channels), "El número de canales no coincide con el número de archivos de entrenamiento."
        assert len(test_files) == len(channels), "El número de canales no coincide con el número de archivos de validación."
except Exception as e:
    print(f"Error: {e}")
    exit()


training_losses = [] 
validation_losses = []

if(cargar_datos_internamente is True):
    model_path_all, training_losses, test_losses = train.train_seg(model.cp.net, train_files=train_files, train_labels_files=train_labels_files, 
                                                                channels=channels, normalize=normalize, test_files=test_files, 
                                                                test_labels_files=test_labels_files, load_files=True, weight_decay=weight_decay, 
                                                                SGD=True, learning_rate=learning_rate, batch_size=batch_size, n_epochs=num_epochs, 
                                                                model_name=nombre_modelo, save_path=destino_reentrenamiento, save_every=guardar_cada, 
                                                                min_train_masks=min_train_masks)
else:
    train_labels = [np.load(fp).astype(np.int32) for fp in train_labels_files] 

    test_labels = [np.load(fp).astype(np.int32) for fp in test_labels_files] 

    train_data = [io.imread(fp) for fp in train_files] 

    test_data = [io.imread(fp) for fp in test_files] 

    model_path_all, training_losses, test_losses = train.train_seg(model.cp.net, train_data=train_data, train_labels=train_labels, 
                                                                channels=channels, normalize=normalize, test_data=test_data, 
                                                                test_labels=test_labels, load_files=False, weight_decay=weight_decay, 
                                                                SGD=True, learning_rate=learning_rate, batch_size=batch_size, n_epochs=num_epochs, 
                                                                model_name=nombre_modelo, save_path=destino_reentrenamiento, save_every=guardar_cada, 
                                                                min_train_masks=min_train_masks)

print("Modelo guardado en:", model_path_all)

exit()

