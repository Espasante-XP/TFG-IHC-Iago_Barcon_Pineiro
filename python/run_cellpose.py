#!/usr/bin/env python
# coding: utf-8


import numpy as np
import time, os, sys
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import matplotlib as mpl
#get_ipython().run_line_magic('matplotlib', 'inline')  #No sé si está bien, esto sale de exportar a python la linea %matplotlib inline, con cualquiera de las 2 líneas me protesta
mpl.rcParams['figure.dpi'] = 300
from cellpose import utils, io

import matplotlib
matplotlib.use('TKAgg')     #Como no se puede ver nada con Qt, he mirado en internet y con este me iría     Source: https://stackoverflow.com/questions/41994485/how-to-fix-could-not-find-or-load-the-qt-platform-plugin-windows-while-using-m





"""
#Lo saqué de Bing
import os
from PIL import Image

def cargar_imagenes(ruta_carpeta):
    imagenes = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith('.jpg') or nombre_archivo.endswith('.png'):  # Asegúrate de poner aquí todos los formatos que quieras cargar
            ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
            imagen = Image.open(ruta_imagen)
            imagenes.append(imagen)
    return imagenes

# Uso de la función
imagenes = cargar_imagenes('ruta/a/tu/carpeta')
"""

imagenes = []

ruta_carpeta = '../Imagenes_para_entrenamiento/IL6_1' 

for nombre_archivo in os.listdir(ruta_carpeta):
    # Asegúrate de poner aquí todos los formatos que quieras cargar
    if nombre_archivo.endswith('.jpg'): # or nombre_archivo.endswith('.png'): 
        ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
        imagenes.append(ruta_imagen)

print("\n")  
print(imagenes)

img2 = io.imread(imagenes[2])


""" Lo he comentado para no tener que cerrar todo el rato la ventana que se abre

plt.figure(figsize=(2,2))
plt.imshow(img2)
plt.axis('off')
plt.show()

"""
print("\n")
print("Se tenía que crear una ventana con la imagen pero ya no lo hago") #Añadido tras comentar lo de arriba
print("\n")





# RUN CELLPOSE

from cellpose import models, io

# DEFINE CELLPOSE MODEL
# model_type='cyto3' or model_type='nuclei'
model = models.Cellpose(gpu=False, model_type='cyto3')

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

channels = [[0,0]] # A lo mejor cambiando algo aquí la cosa mejora



from pycocotools.coco import COCO

annFile = 'IL6_1_prueba.json'

coco=COCO(annFile) # funciona

category_ids = coco.getCatIds()
num_categories = len(category_ids)

# Load images for the given ids
image_ids = coco.getImgIds()

annotation_ids = []
annotations = []

binaryMasks = []

#Se crean las máscaras vacías para las imágenes, hay tantas imágenes (image_ids) como anotaciones (annotation_ids)
for id in image_ids:
    img_info = coco.loadImgs(id)[0]
    height, width = img_info['height'], img_info['width']
    aux = np.zeros((height, width), dtype=np.uint8)
    binaryMasks.append(aux)

index = 0

#Hago la creación de las máscaras en base a las anotaciones en otro bucle para no liarme
for id in image_ids:
    annotation = coco.getAnnIds(imgIds=id)
    annotation_ids.append(annotation) #Revisar más tarde con calma porque creo que no hace falta que sea una lista
    annotations = coco.loadAnns(annotation)
    for annotation in annotations:
        segmentation = annotation['segmentation']
        mask = coco.annToMask(annotation)                #Esta es la función que me dijo Raquel de usar, la función annToMask
        # Add the mask to the binary mask
        binaryMasks[index] += mask
    index = index + 1



#Muestra todas las máscaras cargadas (funciona correctamente)
"""
for mask in binaryMasks:
    # Display the binary mask
    plt.figure(figsize=(10,10))
    plt.imshow(mask, cmap='gray')
    plt.axis('off')
    plt.title('Binary Mask')
    #plt.savefig('binary_mask_Image_1029.png', dpi=300) #El nombre ahora quedó obsoleto de cojones porque se miran todas y no solo una máscara
    plt.show()
"""


import json

archivo_json = '../Valores_para_evaluacion/parametros_model_eval.json'
nombre_diameter = 'diameter'
nombre_min_size = 'min_size'
nombre_normalize = 'normalize'
nombre_niter = 'niter'
nombre_tile_overlap = 'tile_overlap'
nombre_flow_threshold = 'flow_threshold'
nombre_cellprob_threshold = 'cellprob_threshold'
nombre_stitch_threshold = 'stitch_threshold'

archivo_abierto = open(archivo_json)

# Obtener el valor del nombre
valores_parametros_modelo = json.load(archivo_abierto)

print("Valor de diameter en el json = ")
print(valores_parametros_modelo[nombre_diameter])


#Comprobaciones de que los valores cargados son correctos
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


def es_numero(cadena):
    try:
        float(cadena)
        return True
    except ValueError:
        return False


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


texto_valor_stitch_threshold = valores_parametros_modelo[nombre_stitch_threshold]

if(es_numero(texto_valor_stitch_threshold)):
    valor_stitch_threshold = float(texto_valor_stitch_threshold)
elif (texto_valor_stitch_threshold.isalpha() and texto_valor_stitch_threshold == "None"):
    valor_stitch_threshold = None
else:
    print("Error, el valor introducido para la variable stitch_threshold no es válido")
    exit()




from generate_seg_mask import obtener_izquierda_delimitador
from generate_seg_mask import generate_seg_mask

masks_pred = []

indice = 0
for filename in imagenes:
    img2 = io.imread(filename)  # Cambié img por img2
    
    # Utiliza siempre el primer valor de channels
    chan = channels[0]

    masks, flows, styles, diams = model.eval(img2, diameter=valor_diameter, channels=chan, normalize=valor_normalize,
             flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
             stitch_threshold=valor_stitch_threshold, min_size=valor_min_size, niter=valor_niter, tile_overlap=valor_tile_overlap)

    masks_pred.append(masks)

    delim = "."
    nombreArchivo = obtener_izquierda_delimitador(filename, delim)

    nombreArchivo = nombreArchivo + nombre_diameter + texto_valor_diameter #"diamerter350"

    np.save(nombreArchivo, masks, allow_pickle=True)

    urlMascara = nombreArchivo + "_mask.png"

    generate_seg_mask(img2, masks, urlMascara)
    print(f"Se ha generado la máscara {indice}")
    indice = indice + 1

print("\n")
print("Ha acabado la parte de generación de máscaras del modelo")
print("\n")

from PIL import Image

def resize_image(image_array, max_size=512):
    # Convertir el array a una imagen PIL
    img = Image.fromarray(image_array)
    if img.mode not in ('L', 'RGB'):
        img = img.convert('L')
    img.thumbnail((max_size, max_size), Image.LANCZOS) #Image.ANTIALIAS   #Image.LANCZOS   #Image.BICUBIC 
    #Flags que generan imágenes de menor calidad: Image.BILINEAR Image.NEAREST
    # Convertir la imagen PIL redimensionada de vuelta a un array
    resized_image_array = np.array(img)
    return resized_image_array


from cellpose.metrics import aggregated_jaccard_index

resultados_jaccard = []


for index in range(0, len(binaryMasks)):
    # Si no usas una lista dan errores de dividir entre nan o entre 0, no sé por que, es raro, 
    # pero si uso listas no pasa
    true_list_aux = []
    true_list_aux.append(binaryMasks[index])
    pred_list_aux = []
    pred_list_aux.append(masks_pred[index])
    aux = aggregated_jaccard_index(true_list_aux, pred_list_aux)
    resultados_jaccard.append(aux)

for index in range(0, len(resultados_jaccard)):
    print(f"Resultados jaccard {index}")
    print(resultados_jaccard[index])
    print("\n")

#resultado = aggregated_jaccard_index(resized_masks_true, resized_masks_pred)

from cellpose.metrics import boundary_scores

prueba_lista = []

prueba_lista.append(1)

#prueba_lista.append(2)

#prueba_lista.append(4) #Con este tengo que tener los tamaños de las imágenes de 200x200 y la RAM está al límite


resized_masks_true = []
resized_masks_pred = []

# Con 128 funciona pero los valores son una puta mierda, si hay 4 en prueba_lista en boundary_scores
# Con 200 funciona pero me llega la RAM al límite, si hay 4 en boundary_scores (en el viejo, creo)
# Con 300 funciona parece que bien, aunque si hay algo más le cuesta a la memoria, si hay solo 1 en prueba_lista en boundary_scores
# Con 275 va, si hay solo 1 en prueba_lista en boundary_scores
tamanho_escala = 275

for index in range(0, len(binaryMasks)):
    aux = resize_image(binaryMasks[index], tamanho_escala) 
    resized_masks_true.append(aux) 
    aux = resize_image(masks_pred[index], tamanho_escala) 
    resized_masks_pred.append(aux)             


import gc

gc.collect() # Forzar la recolección de basura

#precision, recall, fscore = boundary_scores(resized_masks_true, resized_masks_pred, prueba_lista)

def process_in_batches(masks_true, masks_pred, prueba_lista, batch_size):
    precision_list, recall_list, fscore_list = [], [], []
    for i in range(0, len(masks_true), batch_size):
        batch_true = masks_true[i:i + batch_size]
        batch_pred = masks_pred[i:i + batch_size]
        precision, recall, fscore = boundary_scores(batch_true, batch_pred, prueba_lista)
        precision_list.append(precision)
        recall_list.append(recall)
        fscore_list.append(fscore)
        gc.collect() # Forzar la recolección de basura

    return np.mean(precision_list), np.mean(recall_list), np.mean(fscore_list)

batch_size = 1000  # Ajusta el tamaño del lote según tu memoria disponible

precision = []
recall = []
fscore = []

#Bucle para generar las listas de resultados de las máscaras de la función boundary_scores
for index in range(0, len(resized_masks_true)):
    #Si no usas una lista parece que va mal
    true_list_aux = []
    true_list_aux.append(resized_masks_true[index])
    pred_list_aux = []
    pred_list_aux.append(resized_masks_pred[index])
    gc.collect() # Forzar la recolección de basura
    aux1, aux2, aux3 = boundary_scores(true_list_aux, pred_list_aux, prueba_lista)


    #true_list_aux2 = []
    #true_list_aux2.append(binaryMasks[index])
    #pred_list_aux2 = []
    #pred_list_aux2.append(masks_pred[index])
    #aux1, aux2, aux3 = process_in_batches(true_list_aux2, pred_list_aux2, prueba_lista, batch_size)
    
    
    #precision, recall, fscore = boundary_scores(resized_masks_true, resized_masks_pred, prueba_lista)
    precision.append(aux1)
    recall.append(aux2)
    fscore.append(aux3)
    print(f"ha acabado la evaluación de la máscara {index}")
    gc.collect() # Forzar la recolección de basura


#Función para crear el nombre del archivo donde se guardan las métricas de la imagen
def create_name_metrics_archive(full_name_metrics_archive):
    path_folder_metrics = '../Resultado_metricas/'
    full_path = path_folder_metrics + full_name_metrics_archive
    return full_path


#Función para obtener el nombre de la imagen sin extensión a la que pertenecen las métricas 
# de las imágenes que se encuentran en la carpeta IL6_1
def obtain_image_name(index):
    #Estas son las líneas de más arriba de donde sale la variable image_ids
    #from pycocotools.coco import COCO
    #annFile = 'IL6_1_prueba.json' 
    #coco=COCO(annFile) 
    #image_ids = coco.getImgIds()
    image_id = image_ids[index]  
    image_info = coco.loadImgs(image_id)
    #image_info[0]['file_name']
    nombre_imagen = image_info[0]['file_name']

    from generate_seg_mask import obtener_izquierda_delimitador
    delim = "."
    nombre_imagen_sin_extension = obtener_izquierda_delimitador(nombre_imagen, delim)
    archivo_json = nombre_imagen_sin_extension + ".json"
    return archivo_json


#Creo que voy a hacer un diccionario por imagen, siguiendo el esquema de abajo, el nombre del 
# diccionario exportado será el mismo que el del archivo .npy supongo, revisar con calma.
#El diccionario supongo que lo haré del tipo nombre (de la imagen), jaccard -> valor, precision -> valor, recall -> valor y F-score -> valor


#Bucle para crear los diccionarios, guardar los datos de los diccionarios en archivos .json
for index in range(0, len(binaryMasks)):
    nombre_imagen = obtain_image_name(index)
    path_metricas = create_name_metrics_archive(nombre_imagen)
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
