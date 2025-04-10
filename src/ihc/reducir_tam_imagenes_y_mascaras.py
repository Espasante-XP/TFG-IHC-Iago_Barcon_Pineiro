#!/usr/bin/env python
# coding: utf-8

# Sirve para reducir el tamaño de las imágenes de la carpeta y subcarpetas que estén dentro del directorio indicado en root_resize_directory
# Para modificar los directorios de entrada y salida, así como las extensiones de las imágenes, las extensiones de las máscaras y la escala 
# hay que modificar el archivo ../../config/preprocesado.json


import numpy as np
import os
import cv2
from utils import obter_lista_ficheiros, es_num_positivo_string, es_extension_imagen_string, es_ruta_valida, es_extension_mascara_string, get_final_folder_name
import json
from pathlib import Path
from cellpose import io


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

if(isinstance(texto_valor_dir_imagenes, list)): # Si es una lista de directorios, se comprueba que todos los directorios valgan
    for directorio in texto_valor_dir_imagenes:
        if(not Path(directorio).exists() or not Path(directorio).is_dir()):
            print("Error, el valor introducido para el directorio de imágenes no es válido")
            exit()
    root_resize_directory = texto_valor_dir_imagenes
else:
    if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
        root_resize_directory = texto_valor_dir_imagenes 
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

if(es_extension_mascara_string(texto_valor_ext_mascara)): 
    if(texto_valor_ext_mascara.startswith('.')):
        ext_mascara = texto_valor_ext_mascara
    else:
        ext_mascara = '.' + texto_valor_ext_mascara
    if(ext_mascara == ext_imagenes):
        print("Error, el valor introducido para la extensión de las máscaras y las imágenes es el mismo")
        exit()    
else:
    print("Error, el valor introducido para la extensión de las máscaras no es válido")
    exit()


images_path = []

for directorio in root_resize_directory:
    images_path.extend(obter_lista_ficheiros(directorio, ext_imagenes))

masks_path = []

for directorio in root_resize_directory:
    masks_path.extend(obter_lista_ficheiros(directorio, ext_mascara))


# Crear carpeta de salida principal
if not os.path.exists(output_base_dir):
    os.makedirs(output_base_dir)

# Crear subcarpetas dentro de output_base_dir basadas en root_resize_directory
subfolders = {}
for directory in root_resize_directory:
    # Obtener el nombre de la carpeta final (nombre más a la derecha)
    final_folder_name = get_final_folder_name(directory)
    
    # Crear la subcarpeta en output_base_dir si no existe
    subfolder_path = os.path.join(output_base_dir, final_folder_name)
    if not os.path.exists(subfolder_path):
        os.makedirs(subfolder_path)
    
    # Guardar la relación entre el directorio original y su subcarpeta
    subfolders[directory] = subfolder_path


index = 0
for archivo in masks_path:
    # Mantener la estructura de subcarpetas
    image_path = images_path[index]
    mask_path = archivo

    # Determinar el directorio original donde estaba el archivo
    original_directory = None
    for dir_in_list in root_resize_directory:
        if image_path.startswith(dir_in_list):
            original_directory = dir_in_list
            break

    if original_directory is None:
        print(f"Advertencia: No se pudo determinar el directorio original para {image_path}. Se guardará en la carpeta base.")
        output_dir = output_base_dir
    else:
        # Obtener el nombre de la carpeta final del directorio original
        final_folder_name = get_final_folder_name(original_directory)

        # Usar la carpeta principal creada anteriormente
        output_subfolder = subfolders[original_directory]

        # Construir la ruta relativa dentro del directorio original
        relative_path = os.path.relpath(mask_path, original_directory)
        output_path = os.path.join(output_subfolder, relative_path)

        # Crear los directorios necesarios dentro de la carpeta de salida
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    image_array = io.imread(image_path)
    if ext_mascara == '.npy':
        mask_array = np.load(mask_path)
    else:
        mask_array = io.imread(mask_path)

    resized_image, resized_mask = resize_image_and_mask(image_array, mask_array)

    if ext_mascara == '.npy':
        np.save(output_path, resized_mask, allow_pickle=True)
    else:
        io.imsave(output_path, resized_mask)

    relative_image_path = os.path.relpath(image_path, original_directory)
    output_image_path = os.path.join(output_subfolder, relative_image_path)
    io.imsave(output_image_path, resized_image)

    index += 1

print("Fin del reescalado de las máscaras de ground truth de las imágenes de entrenamiento y/o validación")
