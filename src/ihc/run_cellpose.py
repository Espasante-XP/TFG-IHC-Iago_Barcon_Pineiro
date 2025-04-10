#!/usr/bin/env python
# coding: utf-8


import numpy as np
from pathlib import Path
from cellpose import io, models
from cellpose.metrics import aggregated_jaccard_index, boundary_scores
from generate_seg_mask import obtener_izquierda_delimitador, generate_seg_mask
from utils import obter_lista_ficheiros, es_extension_imagen_string, es_numero
import json
import gc
import os


delim = "."
path_folder_metrics = '../../resultados/'


def create_metrics_name(directory_path):
    # Extraer el nombre del archivo y su directorio
    nombre_imagen = os.path.basename(directory_path)  # Nombre del archivo (con extensión)
    directorio_imagen = os.path.dirname(directory_path)  # Directorio completo donde está la imagen
    
    # Obtener el nombre del directorio final
    folder_name = os.path.basename(directorio_imagen)
    
    # Eliminar la extensión del nombre de la imagen
    nombre_imagen_sin_extension, _ = os.path.splitext(nombre_imagen)
    
    # Crear la ruta completa para la nueva carpeta dentro de path_folder_metrics
    metrics_folder_path = os.path.join(path_folder_metrics, folder_name)
    
    # Asegurarse de que la carpeta exista, si no, crearla
    os.makedirs(metrics_folder_path, exist_ok=True)
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


archivo_json = '../../config/modelo_cellpose.json'

nombre_dir_imagenes = 'path_imagenes'
nombre_dir_modelo = 'path_modelo'
nombre_ext_imagenes = 'extension_imagen'
nombre_channels = 'channels'
nombre_diameter = 'diameter'
nombre_min_size = 'min_size'
nombre_normalize = 'normalize'
nombre_niter = 'niter'
nombre_tile_overlap = 'tile_overlap'
nombre_flow_threshold = 'flow_threshold'
nombre_cellprob_threshold = 'cellprob_threshold'
nombre_sufijo_mascara_pred = 'nombre_sufijo_mascara_pred'
nombre_sufijo_mascara_g_truth = 'sufijo_mascara_g_truth'

archivo_abierto = open(archivo_json)

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_dir_imagenes = valores_parametros_modelo[nombre_dir_imagenes]
if(isinstance(texto_valor_dir_imagenes, list)): # Si es una lista de directorios, se comprueba que todos los directorios valgan
    for directorio in texto_valor_dir_imagenes:
        if(not Path(directorio).exists() or not Path(directorio).is_dir()):
            print("Error, el valor introducido para el directorio de imágenes no es válido")
            exit()
    root_images_directory = texto_valor_dir_imagenes
else:
    if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
        root_images_directory = texto_valor_dir_imagenes 
    else:
        print("Error, el valor introducido para el directorio de imágenes no es válido")
        exit()


texto_valor_dir_modelo = valores_parametros_modelo[nombre_dir_modelo]

if(Path(texto_valor_dir_modelo).exists()): 
    model_file_path = texto_valor_dir_modelo 
else:
    print("Error, el valor introducido para el path al modelo no es válido")
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


texto_valor_diameter = valores_parametros_modelo[nombre_diameter]

if(texto_valor_diameter.isdigit()):
    if(int(texto_valor_diameter) >= 0):
        valor_diameter = int(texto_valor_diameter)
    else:
        print("Error, el valor introducido para la variable diameter no es válido")
        exit()
elif ((texto_valor_diameter.isalpha() and texto_valor_diameter == "None") or (texto_valor_diameter == "")):
    valor_diameter = None
    print("Warning: No se ha especificado un valor para el diámetro, el modelo estimará el valor")
else:
    print("Error, el valor introducido para la variable diameter no es válido")
    exit()
       

texto_valor_min_size = valores_parametros_modelo[nombre_min_size]

if(texto_valor_min_size.isdigit()):
    if(int(texto_valor_min_size) >= 0):
        valor_min_size = int(texto_valor_min_size)
    else:
        print("Error, el valor introducido para la variable min_size no es válido")
        exit()
    if(((valor_min_size > valor_diameter) and (valor_diameter is not None)) or ((valor_min_size >= 0) and (valor_diameter is None))):
        print("Warning: el valor de la variable min_size es mayor que el valor de la variable diameter")
elif ((texto_valor_min_size.isalpha() and texto_valor_min_size == "None") or (texto_valor_min_size == "")):
    valor_min_size = None
else:
    print("Error, el valor introducido para la variable min_size no es válido")
    exit()


texto_valor_normalize = valores_parametros_modelo[nombre_normalize]

if(texto_valor_normalize.isalpha() and texto_valor_normalize == "True"):
    valor_normalize = True
elif (texto_valor_normalize.isalpha() and texto_valor_normalize == "False"):
    valor_normalize = False
else:
    print("Error, el valor introducido para la variable normalize no es válido")
    exit()


texto_valor_niter = valores_parametros_modelo[nombre_niter]

if(texto_valor_niter.isdigit()):
    valor_niter = int(texto_valor_niter)
elif (texto_valor_niter.isalpha() and texto_valor_niter == "None"):
    valor_niter = None
else:
    print("Error, el valor introducido para la variable niter no es válido")
    exit()


texto_valor_tile_overlap = valores_parametros_modelo[nombre_tile_overlap]

if(es_numero(texto_valor_tile_overlap)):
    valor_tile_overlap = float(texto_valor_tile_overlap)
elif (texto_valor_tile_overlap.isalpha() and texto_valor_tile_overlap == "None"):
    valor_tile_overlap = None
else:
    print("Error, el valor introducido para la variable tile_overlap no es válido")
    exit()


texto_valor_flow_threshold = valores_parametros_modelo[nombre_flow_threshold]

if(es_numero(texto_valor_flow_threshold)):
    valor_flow_threshold = float(texto_valor_flow_threshold)
elif (texto_valor_flow_threshold.isalpha() and texto_valor_flow_threshold == "None"):
    valor_flow_threshold = None
else:
    print("Error, el valor introducido para la variable flow_threshold no es válido")
    exit()


texto_valor_cellprob_threshold = valores_parametros_modelo[nombre_cellprob_threshold]

if(es_numero(texto_valor_cellprob_threshold)):
    valor_cellprob_threshold = float(texto_valor_cellprob_threshold)
elif (texto_valor_cellprob_threshold.isalpha() and texto_valor_cellprob_threshold == "None"):
    valor_cellprob_threshold = None
else:
    print("Error, el valor introducido para la variable cellprob_threshold no es válido")
    exit()


texto_valor_sufijo_mascara_pred = valores_parametros_modelo[nombre_sufijo_mascara_pred]
if(isinstance(texto_valor_sufijo_mascara_pred, str)):
    if(texto_valor_sufijo_mascara_pred == ""):
        sufijo_mascara_pred = "_predicted_mask"
    else:
        sufijo_mascara_pred = texto_valor_sufijo_mascara_pred    
else:
    print("Error, el valor introducido para el sufijo de las máscaras predecidas por el modelo no es válido")
    exit()


texto_valor_sufijo_mascara = valores_parametros_modelo[nombre_sufijo_mascara_g_truth]
if(isinstance(texto_valor_sufijo_mascara, str)):
    sufijo_mascara_ground_truth = texto_valor_sufijo_mascara
else:
    print("Error, el valor introducido para el sufijo de la máscara ground_truth no es válido")
    exit()


imagenes = []

for directorio in root_images_directory:
    imagenes.extend(obter_lista_ficheiros(directorio, ext_imagenes))

try:
    if (es_lista_de_listas):
        assert len(imagenes) == len(channels), "El número de imágenes no coincide con el número de canales especificados."
except Exception as e:
    print(f"Error: {e}")
    exit()


try: 
    model = models.CellposeModel(gpu=True, pretrained_model=model_file_path)
except Exception as e:
    print(f"Error: {e}")
    print("No se ha podido cargar el modelo")
    exit()


masks_pred = []
indice = 0    
for filename in imagenes:
    imagen_cargada = io.imread(filename)  

    if(valor_min_size is None):
        resultado = model.eval(imagen_cargada, diameter=valor_diameter, channels=channels, normalize=valor_normalize,
                flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
                niter=valor_niter, tile_overlap=valor_tile_overlap, progress=True)
    else:     
        resultado = model.eval(imagen_cargada, diameter=valor_diameter, channels=channels, normalize=valor_normalize,
             flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
            min_size=valor_min_size, niter=valor_niter, tile_overlap=valor_tile_overlap, progress=True)

    if len(resultado) == 3: 
        masks, flows, styles = resultado 
    else: 
        masks, flows, styles, diams = resultado

    masks_pred.append(masks)

    nombreArchivo = obtener_izquierda_delimitador(filename, delim)

    nombreArchivo = nombreArchivo + sufijo_mascara_pred 

    np.save(nombreArchivo, masks, allow_pickle=True)

    urlMascara = nombreArchivo + "_mask.png"

    generate_seg_mask(imagen_cargada, masks, urlMascara)
    print(f"Se ha generado la máscara {indice}")
    indice = indice + 1

print("\n")
print("Ha acabado la parte de generación de máscaras del modelo")
print("\n")


del nombre_diameter, nombre_min_size, nombre_normalize, nombre_niter, nombre_tile_overlap, valor_normalize, valor_diameter
del nombre_cellprob_threshold, nombre_flow_threshold, channels, valor_flow_threshold, valor_cellprob_threshold, valor_min_size
del valor_niter, valor_tile_overlap, nombreArchivo, urlMascara, indice, masks, imagen_cargada, archivo_abierto, valores_parametros_modelo

if len(resultado) == 3: 
    del filename, flows, styles, model, resultado
else: 
    del filename, flows, styles, diams, model, resultado 


path_anotaciones_coco = root_images_directory

lista_anotaciones_mascaras = []

for directorio in path_anotaciones_coco:
    lista_anotaciones_mascaras.extend(obter_lista_ficheiros(directorio, '.npy', sufijo_mascara_ground_truth)) 


try:
    assert len(masks_pred) == len(lista_anotaciones_mascaras), "El número de máscaras ground truth no coincide con el número de máscaras predichas."
except Exception as e:
    print(f"Error: {e}")
    exit()

resultados_jaccard = []

for mascara_pred, ground_truth in zip(masks_pred, lista_anotaciones_mascaras):    
    true_list_aux = []
    true_list_aux.append(np.load(ground_truth))
    pred_list_aux = []
    pred_list_aux.append(mascara_pred) 
    aux = aggregated_jaccard_index(true_list_aux, pred_list_aux)
    resultados_jaccard.append(aux)

for index in range(0, len(resultados_jaccard)):
    print(f"Resultados jaccard {index}: {imagenes[index]}")
    print(resultados_jaccard[index])

print("\n")
print("Se realizaron las anotaciones jaccard de las imágenes")
print("La mediana de las anotaciones es ", np.median(resultados_jaccard))
print("\n")

del archivo_json, true_list_aux, pred_list_aux, aux

gc.collect() 

precision = []
recall = []
fscore = []

axis_scale = []
axis_scale.append(1)
index = 0
#Bucle para generar las listas de resultados de las máscaras de la función boundary_scores  
for mascara_pred, ground_truth in zip(masks_pred, lista_anotaciones_mascaras):    
    true_list_aux = []
    true_list_aux.append(np.load(ground_truth))
    pred_list_aux = []
    pred_list_aux.append(mascara_pred) 
    gc.collect()
    aux1, aux2, aux3 = boundary_scores(true_list_aux, pred_list_aux, axis_scale)
    precision.append(aux1)
    recall.append(aux2)
    fscore.append(aux3)
    print(f"ha acabado la evaluación de la máscara {index}: {imagenes[index]}")
    index = index + 1
    gc.collect()


print("\n")
print("Se han generado todas las métricas boundary_scores de las máscaras")

#Bucle para crear los diccionarios, guardar los datos de los diccionarios en archivos .json
index = 0
for imagen in imagenes:
    path_metricas = create_metrics_name(imagen)
    data = {}
    with open(path_metricas, 'w') as file: 
        # Escribir el diccionario vacío en el archivo
        json.dump(data, file)
    data['jaccard'] = resultados_jaccard[index]
    data['precision'] = precision[index]
    data['recall'] = recall[index]
    data['fscore'] = fscore[index]
    data_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in data.items()}
    with open(path_metricas, 'w') as file:
    # Escribir el diccionario en el archivo
        json.dump(data_serializable, file)
    index = index + 1    


print("Se han creado todos los archivos JSON")

exit()