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


#Añadido por mi para que carguen las imágenes de una carpeta
import os
from PIL import Image

# I will download images from website
#urls = ['http://www.cellpose.org/static/images/img02.png',
 #       'http://www.cellpose.org/static/images/img03.png',
  #      'http://www.cellpose.org/static/images/img05.png']

#files = ['./CellPose_test/test/000_img.png']
files = ['./Imagenes_para_entrenamiento/IL6_1/Image_1033.jpg']


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

#i = 0
for nombre_archivo in os.listdir(ruta_carpeta):
    # Asegúrate de poner aquí todos los formatos que quieras cargar
    if nombre_archivo.endswith('.jpg'): # or nombre_archivo.endswith('.png'): 
        ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
        imagenes.append(ruta_imagen)
  
#for url in urls:
 #   parts = urlparse(url)
  #  filename = os.path.basename(parts.path)
   # if not os.path.exists(filename):
    #    sys.stderr.write('Downloading: "{}" to {}\n'.format(url, filename))
     #   utils.download_url_to_file(url, filename)
    #files.append(filename)


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

#No me acuerdo ni por que está
print(imagenes)



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

channels = [[0,0]] #, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]

# He quitado todos los canales menos uno, a ver si aún así saca todas las máscaras

# if diameter is set to None, the size of the cells is estimated on a per image basis
# you can set the average cell `diameter` in pixels yourself (recommended) 
# diameter can be a list or a single number for all images

# you can run all in a list e.g.
# >>> imgs = [io.imread(filename) in for filename in files]
# >>> masks, flows, styles, diams = model.eval(imgs, diameter=None, channels=channels)
# >>> io.masks_flows_to_seg(imgs, masks, flows, diams, files, channels)
# >>> io.save_to_png(imgs, masks, flows, files)

# or in a loop
#for chan, filename in zip(channels, files): #files es del viejo donde solo se usa la 33
#for chan, filename in zip(channels, imagenes):
    
    #img2 = io.imread(filename) #Cambié img por img2
    #print(filename)
    
    #masks, flows, styles, diams = model.eval(img2, diameter=None, channels=chan)

    # save results so you can load in gui
    #io.masks_flows_to_seg(img2, masks, flows, filename, channels=chan, diams=diams)

    # save results as png
    #io.save_to_png(img2, masks, flows, filename)



from pycocotools.coco import COCO

annFile = 'IL6_1_prueba.json'

coco=COCO(annFile) # funciona

category_ids = coco.getCatIds()
num_categories = len(category_ids)

# Load images for the given ids
image_ids = coco.getImgIds()

#Esta línea de abajo la tengo que cambiar para que se metan todos los valores en una lista de image_id o algo así y luego con 
# eso haría el bucle o algo
image_id = image_ids[0]  # Change this line to display a different image
image_info = coco.loadImgs(image_id)

annotation_ids = []
annotations = []

binaryMasks = []

#Se crean las máscaras vacías para las imágenes, hay tantas imágenes (image_ids) como anotaciones (annotation_ids)
for id in image_ids:
    img_info = coco.loadImgs(id)[0]
    height, width = img_info['height'], img_info['width']
    aux = np.zeros((height, width), dtype=np.uint8)
    binaryMasks.append(aux)

#[HECHO] Creo que tengo que hacer 2 bucles, el de fuera con los valores de annotation_ids y el de dentro como este que hay pero  
# en binaryMasks[index] el valor de index creo que tiene que ser el número de iteración del bucle grande en el bucle grande

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

archivo_abierto = open(archivo_json)

# Obtener el valor del nombre
valores_parametros_modelo = json.load(archivo_abierto)

print("Valor de diameter en el json = ")
print(valores_parametros_modelo[nombre_diameter])

texto_valor_diameter = valores_parametros_modelo[nombre_diameter]

valor_diameter = int(texto_valor_diameter)

from generate_seg_mask import obtener_izquierda_delimitador
from generate_seg_mask import generate_seg_mask

masks_pred = []

for filename in imagenes:
    img2 = io.imread(filename)  # Cambié img por img2
    
    # Utiliza siempre el primer valor de channels
    chan = channels[0]

    masks, flows, styles, diams = model.eval(img2, diameter=valor_diameter, channels=chan) #diameter=None

    masks_pred.append(masks)

    delim = "."
    nombreArchivo = obtener_izquierda_delimitador(filename, delim)

    nombreArchivo = nombreArchivo + nombre_diameter + texto_valor_diameter #"diamerter350"

    np.save(nombreArchivo, masks, allow_pickle=True)

    urlMascara = nombreArchivo + "_mask.png"

    generate_seg_mask(img2, masks, urlMascara)

print("\n")
print("Ha acabado la parte de generación de máscaras del modelo")
print("\n")

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


resized_masks_true = []
resized_masks_pred = []

for index in range(0, len(binaryMasks)):
    aux = resize_image(binaryMasks[index], 150) # Con 128 funciona pero los valores son una puta mierda
    resized_masks_true.append(aux) # Con 200 funciona pero me llega la RAM al límite
    aux = resize_image(masks_pred[index], 150) 
    resized_masks_pred.append(aux) 

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

prueba_lista.append(2)

#prueba_lista.append(4) #Con este tengo que tener los tamaños de las imágenes de 200x200 y la RAM está al límite


# Hacer el bucle donde se guardarán en listas todos los valores que salen de la función boundary_scores
# Hacer 2 variables auxiliares para que sean listas de un elemento con las máscaras

#precision, recall, fscore = boundary_scores(resized_masks_true, resized_masks_pred, prueba_lista)

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
    aux1, aux2, aux3 = boundary_scores(true_list_aux, pred_list_aux, prueba_lista)
    #precision, recall, fscore = boundary_scores(resized_masks_true, resized_masks_pred, prueba_lista)
    precision.append(aux1)
    recall.append(aux2)
    fscore.append(aux3)


#Tengo que hacer el bucle para pillar con las anotaciones el nombre de la imagen, quitarle el .jpg
# y crear el nombre completo para guardarlo en una lista y usarlo luego para exportar los diccionarios.
# Creo el diccionario en el bucle para no hacer una lista con todos los diccionarios si no que así solo
# tengo que reutilizar y exportar el diccionario, espero que funcione

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


#Bucle para crear los diccionarios, guardar los datos de los diccionarios en 
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


"""
import json
#tengo que tener abierto el archivo, es decir, el archivo debe existir para poder guardarlo, mirar como hacer 
# https://pythones.net/diccionarios-en-python/

data = {}

# Abrir (o crear) un archivo JSON en modo de escritura
with open('Image_1029diamerter300.json', 'w') as file:
    # Escribir el diccionario vacío en el archivo
    json.dump(data, file)

print("Archivo JSON vacío creado exitosamente.")

data['jaccard'] = resultados_jaccard[0]

data_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in data.items()}

with open('Image_1029diamerter300.json', 'w') as file:
    # Escribir el diccionario vacío en el archivo
    json.dump(data_serializable, file)

print("AL archivo JSON se le han agregado datos")

"""


"""
print('Mask = ')
print(type(masks))
print(masks)

print('Flows = ')
print(type(flows))
print(flows)

print('Img2 = ')
print(type(img2))
print(img2)

print('Filename = ')
print(type(filename))
print(filename)

# DISPLAY RESULTS
from cellpose import plot

fig = plt.figure(figsize=(12,5))

plot.show_segmentation(fig, img2, masks, flows[0], channels=chan)
plt.tight_layout()
plt.show()

"""


