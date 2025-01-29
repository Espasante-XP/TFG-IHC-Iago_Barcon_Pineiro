#!/usr/bin/env python
# coding: utf-8


# Sirve para reducir el tamaño de las imágenes de la carpeta y subcarpetas que estén dentro del directorio indicado en root_resize_directory

import numpy as np
import os
import cv2
from utils import obter_lista_ficheiros, es_num_positivo_string, es_extension_imagen_string, es_ruta_valida
import json
from pathlib import Path


scale = 1.0

def resize_image_and_mask(image_array, mask_array): 
    # Obtener las dimensiones originales de la imagen
    height, width = image_array.shape[:2]

    new_width = int(width * scale)
    new_height = int(height * scale)

    resized_image_array = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    resized_mask_array = cv2.resize(mask_array, (new_width, new_height), interpolation=cv2.INTER_NEAREST) 
    
    return resized_image_array, resized_mask_array



archivo_json = '../../config/preprocesado.json'

archivo_abierto = open(archivo_json)

nombre_dir_imagenes = 'path_imagenes'

nombre_dir_salida = 'path_salida'

nombre_escala = 'escala'

nombre_ext_imagenes = 'extension_imagen'

nombre_ext_mascara = 'extension_mascara'

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_escala = valores_parametros_modelo[nombre_escala]

if(es_num_positivo_string(texto_valor_escala)):
    scale = float(texto_valor_escala)
else:
    print("Error, el valor introducido para la variable escala no es válido")
    exit()


texto_valor_dir_imagenes = valores_parametros_modelo[nombre_dir_imagenes]

if(Path(texto_valor_dir_imagenes).exists() & Path(texto_valor_dir_imagenes).is_dir()):
    root_resize_directory = Path(texto_valor_dir_imagenes)
else:
    print("Error, el valor introducido para el directorio de imágenes no es válido")
    exit()


texto_valor_dir_salida = valores_parametros_modelo[nombre_dir_salida]

if(es_ruta_valida(texto_valor_dir_salida)):
    output_base_dir = texto_valor_dir_salida 
else:
    print("Error, el valor introducido para el directorio de salida no es válido")
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

if(texto_valor_ext_mascara.lower().lstrip('.') == 'npy'): 
    if(texto_valor_ext_mascara.startswith('.')):
        ext_mascara = texto_valor_ext_mascara
    else:
        ext_mascara = '.' + texto_valor_ext_mascara
else:
    print("Error, el valor introducido para la extensión de las máscaras no es válido")
    exit()


image_path = []

image_path = obter_lista_ficheiros(root_resize_directory, ext_imagenes)

mask_path = []

mask_path = obter_lista_ficheiros(root_resize_directory, ext_mascara)

# Crear carpeta de salida 
if not os.path.exists(output_base_dir): 
    os.makedirs(output_base_dir)

index = 0

for archivos in mask_path:

    # Mantener la estructura de subcarpetas 
    relative_path = os.path.relpath(archivos, root_resize_directory) 
    output_path = os.path.join(output_base_dir, relative_path) 
    # Crear los directorios nuevos dentro de la carpeta de salida en caso de no existir
    output_dir = os.path.dirname(output_path) 
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir) 

    image_array = cv2.imread(image_path[index])

    mask_array = np.load(archivos)

    resized_image, resized_mask = resize_image_and_mask(image_array, mask_array) 

    np.save(output_path, resized_mask, allow_pickle=True) 

    relative_image_path = os.path.relpath(image_path[index], root_resize_directory)

    output_image_path = os.path.join(output_base_dir, relative_image_path)

    cv2.imwrite(output_image_path, resized_image) 

    index = index + 1

print("Fin del reescalado de las máscaras de ground truth de las imágenes de entrenamiento o validación")    