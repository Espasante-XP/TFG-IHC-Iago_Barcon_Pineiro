#!/usr/bin/env python
# coding: utf-8

# Se leen las anotaciones en formato COCO de un archivo json y se generan las máscaras correspondientes a cada imagen como archivos .npy y .png
# Para generar cada máscara hay que cambiar los directorios de las imágenes y las anotaciones en ../../config/anotaciones_coco.json


import numpy as np
from cellpose import io
from utils import obter_lista_ficheiros, obtener_carpetas, es_extension_imagen_string, es_alfanumerico_o_guion_bajo
from generate_seg_mask import obtener_izquierda_delimitador
from cargar_anotaciones import cargar_anotaciones_coco_de_archivo
import json 
from pathlib import Path


ext_anotaciones = '.json'
ext_imagen_mascara = '.png'
delim = "."


archivo_json = '../../config/anotaciones_coco.json'

archivo_abierto = open(archivo_json)

nombre_dir_imagenes = 'path_imagenes'

nombre_dir_anotaciones = 'path_anotaciones'

nombre_ext_imagenes = 'extension_imagen'

nombre_sufijo_mascara = 'sufijo_mascara'

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_dir_imagenes = valores_parametros_modelo[nombre_dir_imagenes]

if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
    root_images_directory = texto_valor_dir_imagenes
else:
    print("Error, el valor introducido para el directorio de entrenamiento no es válido")
    exit()


texto_valor_dir_anotaciones = valores_parametros_modelo[nombre_dir_anotaciones]

if(Path(texto_valor_dir_anotaciones).exists() and Path(texto_valor_dir_anotaciones).is_dir()):
    root_anotation_directory = texto_valor_dir_anotaciones
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

texto_valor_sufijo_mascara = valores_parametros_modelo[nombre_sufijo_mascara]

if(es_alfanumerico_o_guion_bajo(texto_valor_sufijo_mascara)):
    sufijo_mascara = '_' + texto_valor_sufijo_mascara
else:
    print("Error, el valor introducido para el sufijo de las máscaras no es válido")
    exit()


rutas_relativas_imagenes = obtener_carpetas(root_images_directory)

index = 0

for ruta_carpeta in rutas_relativas_imagenes:
    
    rutas_anotaciones = root_anotation_directory + ruta_carpeta

    anotaciones = obter_lista_ficheiros(rutas_anotaciones, ext_anotaciones) 

    if not anotaciones:
        print(f"No se han encontrado anotaciones en la ruta: {rutas_anotaciones}")
        exit()

    for anotacion in anotaciones:

        index = 0 

        ruta_imagenes = root_images_directory + ruta_carpeta

        coco, mascaras_multietiqueta, informacion_imagenes = cargar_anotaciones_coco_de_archivo(anotacion)

        for imagen in informacion_imagenes:

            path_imagen = ruta_imagenes + imagen

            mask = mascaras_multietiqueta[index]

            nombre_archivo_anotaciones = obtener_izquierda_delimitador(path_imagen, delim)

            nombre_archivo_anotaciones = nombre_archivo_anotaciones + sufijo_mascara

            np.save(nombre_archivo_anotaciones, mask, allow_pickle=True) 

            nombre_archivo_imagen = nombre_archivo_anotaciones + ext_imagen_mascara

            io.imsave(nombre_archivo_imagen, mask)

            index = index + 1

print(f"Se han guardado todas las máscaras multietiqueta en formato .npy y en formato {ext_imagen_mascara}")

exit()
