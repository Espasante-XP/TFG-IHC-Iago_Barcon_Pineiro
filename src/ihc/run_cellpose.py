#!/usr/bin/env python
# coding: utf-8



import matplotlib
matplotlib.use('TKAgg')     #Como no se puede ver nada con Qt, he mirado en internet y con este me iría     Source: https://stackoverflow.com/questions/41994485/how-to-fix-could-not-find-or-load-the-qt-platform-plugin-windows-while-using-m
import numpy as np
from pathlib import Path
from cellpose import io, models
from cellpose.metrics import aggregated_jaccard_index, boundary_scores
from generate_seg_mask import obtener_izquierda_delimitador, generate_seg_mask
from utils import obter_lista_ficheiros, es_extension_imagen_string, es_numero
from cargar_anotaciones import cargar_anotaciones_coco_de_archivo
import json
import gc
import cv2


scale = 0.25
delim = "."
path_folder_metrics = '../../resultados/'


def resize_image(mask_array):
   
    height, width = mask_array.shape[:2]

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_mask_array = cv2.resize(mask_array, (new_width, new_height), interpolation=cv2.INTER_NEAREST)
    return resized_mask_array 


#Función para obtener el nombre de la imagen sin extensión a la que pertenecen las métricas 
# de las imágenes que se encuentran en la carpeta IL6_1
def create_metrics_name(coco, index): 
    image_ids = coco.getImgIds()
    image_info = coco.loadImgs(image_ids[index])
    nombre_imagen = image_info[0]['file_name']
    nombre_imagen_sin_extension = obtener_izquierda_delimitador(nombre_imagen, delim)
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    full_path = path_folder_metrics + full_name_metrics_archive
    return full_path



# define CHANNELS to run segementation on
# grayscale=0, R=1, G=2, B=3
# channels = [cytoplasm, nucleus]
# if NUCLEUS channel does not exist, set the second channel to 0
# channels = [0,0]
# IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
# channels = [0,0] # IF YOU HAVE GRAYSCALE
# channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus
# channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus

# or if you have different types of channels in each image
#channels = [[2,3], [0,0], [0,0]]

#channels = [[0,0]] # A lo mejor cambiando algo aquí la cosa mejora











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

archivo_abierto = open(archivo_json)

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_dir_imagenes = valores_parametros_modelo[nombre_dir_imagenes]

if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
    root_images_directory = texto_valor_dir_imagenes 
else:
    print("Error, el valor introducido para el directorio de imágenes no es válido")
    exit()


texto_valor_dir_modelo = valores_parametros_modelo[nombre_dir_modelo]

if(Path(texto_valor_dir_modelo).exists()): # and Path(texto_valor_dir_modelo).is_dir()
    model_file_path = texto_valor_dir_modelo 
else:
    print("Error, el valor introducido para el path al modelo no es válido")
    exit()
    # Aquí mejor hacer que si no se pilla uno correcto luego se salte esa parte del código y listo

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

if(isinstance(valor_channels, list)): 

    channels = valor_channels 
else:
    print(f"Error, el valor introducido para la variable {nombre_channels} no es válido")
    exit()


texto_valor_diameter = valores_parametros_modelo[nombre_diameter]

if(texto_valor_diameter.isdigit()):
    valor_diameter = int(texto_valor_diameter)
elif (texto_valor_diameter.isalpha() and texto_valor_diameter == "None"):
    valor_diameter = None
else:
    print("Error, el valor introducido para la variable diameter no es válido")
    exit()


texto_valor_min_size = valores_parametros_modelo[nombre_min_size]

if(texto_valor_min_size.isdigit()):
    valor_min_size = int(texto_valor_min_size)
elif (texto_valor_min_size.isalpha() and texto_valor_min_size == "None"):
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


imagenes = []

imagenes = obter_lista_ficheiros(root_images_directory, ext_imagenes)


#tengo que borrar esto de abajo

path_modelo_reentrenado = '../../models/modelo-channels_[0, 1]-normalize_True-weight_decay_0.0001-learning_rate_0.01-batch_size_8-num_epochs_100-guardar_cada_10-min_train_masks_1'


#path_modelo_reentrenado = '../models/mi_modelo_reentrenado_todas_las_imagenes_5000epochs'

model = models.CellposeModel(gpu=True, model_type='cyto3')

#model.net.load_model(path_modelo_reentrenado)

model.net.load_model(model_file_path)



sufijo_mascara = "-" + "diameter" + "_" + texto_valor_diameter + "-" + "min_size" + "_" + texto_valor_min_size + "-" + "normalize" + "_" + texto_valor_normalize + "-" + "niter" + "_" + texto_valor_niter + "-" + "tile_overlap" + "_" + texto_valor_tile_overlap + "-" + "flow_threshold" + "_" + texto_valor_flow_threshold + "-" + "cellprob_threshold" + "_" + texto_valor_cellprob_threshold

sufijo_mascara = sufijo_mascara.replace('.', '--')

#print("sufijo_mascara: ", sufijo_mascara)


masks_pred = []

indice = 0    

for filename in imagenes:
    imagen_cargada = io.imread(filename)  
    
    # Utiliza siempre el primer valor de channels
    #chan = channels[0]

    resultado = model.eval(imagen_cargada, diameter=valor_diameter, channels=channels, normalize=valor_normalize,
             flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
            min_size=valor_min_size, niter=valor_niter, tile_overlap=valor_tile_overlap, progress=True)

    if len(resultado) == 3: 
        masks, flows, styles = resultado 
    else: 
        masks, flows, styles, diams = resultado

    masks_pred.append(masks)

    nombreArchivo = obtener_izquierda_delimitador(filename, delim)

    nombreArchivo = nombreArchivo + nombre_diameter + texto_valor_diameter

    #nombreArchivo = nombreArchivo + sufijo_mascara

    #print("nombreArchivo: ", nombreArchivo)

    #print(f"Longitud del nombre del archivo: {len(str(nombreArchivo))}")

    #exit()

    np.save(nombreArchivo, masks, allow_pickle=True)

    urlMascara = nombreArchivo + "_mask.png"

    generate_seg_mask(imagen_cargada, masks, urlMascara)
    print(f"Se ha generado la máscara {indice}")
    indice = indice + 1

print("\n")
print("Ha acabado la parte de generación de máscaras del modelo")
print("\n")

#exit()

#Prueba eliminar variables 1

del archivo_json, nombre_diameter, nombre_min_size, nombre_normalize, nombre_niter, nombre_tile_overlap, valor_normalize, valor_diameter
del nombre_cellprob_threshold, nombre_flow_threshold, channels, valor_flow_threshold, valor_cellprob_threshold, valor_min_size
del valor_niter, valor_tile_overlap, nombreArchivo, urlMascara, indice, imagenes, masks, imagen_cargada, archivo_abierto, valores_parametros_modelo

if len(resultado) == 3: 
    del filename, flows, styles, model, resultado
else: 
    del filename, flows, styles, diams, model, resultado 


nombre_anotaciones_coco = "anotaciones_coco"

archivo_abierto = open(archivo_json)

valores_parametros_modelo = json.load(archivo_abierto)

# Cambiarlo para que se escoja un directorio en vez de el archivo y para que se pille el archivo .json de dentro del directorio
texto_valor_anotaciones_coco = valores_parametros_modelo[nombre_anotaciones_coco]

if(Path(texto_valor_anotaciones_coco).exists()): 
    path_anotaciones_coco = texto_valor_anotaciones_coco 
else:
    print("Error, el valor introducido para el path al modelo no es válido")
    exit()




anotaciones_coco = 'anotaciones_coco_enviadas/IL6_1/IL6_1_coco.json' 




coco, mascaras_multietiqueta, informacion_imagenes = cargar_anotaciones_coco_de_archivo(anotaciones_coco)




resultados_jaccard = []

for index in range(0, len(mascaras_multietiqueta)):
    # Si no usas una lista dan errores de dividir entre nan o entre 0, no sé por que, es raro, 
    # pero si uso listas no pasa
    true_list_aux = []
    true_list_aux.append(mascaras_multietiqueta[index])
    pred_list_aux = []
    pred_list_aux.append(masks_pred[index])
    aux = aggregated_jaccard_index(true_list_aux, pred_list_aux)
    resultados_jaccard.append(aux)

for index in range(0, len(resultados_jaccard)):
    print(f"Resultados jaccard {index}")
    print(resultados_jaccard[index])
    print("\n")

#resultado = aggregated_jaccard_index(resized_masks_true, resized_masks_pred)


#Prueba eliminar variables 2
del true_list_aux, pred_list_aux, aux, index



prueba_lista = []

prueba_lista.append(1)

#prueba_lista.append(2)

#prueba_lista.append(4) #Con este tengo que tener los tamaños de las imágenes de 200x200 y la RAM está al límite


resized_masks_true = []
resized_masks_pred = []


for index in range(0, len(mascaras_multietiqueta)):
    aux = resize_image(mascaras_multietiqueta[index]) 
    resized_masks_true.append(aux) 
    aux = resize_image(masks_pred[index])
    resized_masks_pred.append(aux)             


gc.collect() # Forzar la recolección de basura


precision = []
recall = []
fscore = []

#Bucle para generar las listas de resultados de las máscaras de la función boundary_scores
for index in range(0, len(resized_masks_true)):
    true_list_aux = []
    true_list_aux.append(resized_masks_true[index])
    pred_list_aux = []
    pred_list_aux.append(resized_masks_pred[index])
    gc.collect() # Forzar la recolección de basura
    aux1, aux2, aux3 = boundary_scores(true_list_aux, pred_list_aux, prueba_lista)

    precision.append(aux1)
    recall.append(aux2)
    fscore.append(aux3)
    print(f"ha acabado la evaluación de la máscara {index}")
    gc.collect() # Forzar la recolección de basura






#Creo que voy a hacer un diccionario por imagen, siguiendo el esquema de abajo, el nombre del 
# diccionario exportado será el mismo que el del archivo .npy supongo, revisar con calma.
#El diccionario supongo que lo haré del tipo nombre (de la imagen), jaccard -> valor, precision -> valor, recall -> valor y F-score -> valor

image_ids = coco.getImgIds()

#Bucle para crear los diccionarios, guardar los datos de los diccionarios en archivos .json
for index in range(0, len(mascaras_multietiqueta)):
    image_info = coco.loadImgs(image_ids[index])
    path_metricas = create_metrics_name(coco, index)
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

print("\n")
print("Se han creado todos los archivos JSON")
print("\n")

exit()



# Mirar de hacer lo que puso Copilot de utilizar del para borrar las variables que ya no use y así, de paso, 
# ver si hago que se utilice menos memoria en el programa.

# Primero guardar con un commit los valores, si eso en una rama que sea pruebas o algo así, no en la principal.
# Probar con diameter 400 y comparar con los resultados con diameter 300
