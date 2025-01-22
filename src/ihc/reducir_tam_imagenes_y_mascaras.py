#!/usr/bin/env python
# coding: utf-8


# Sirve para reducir el tamaño de las imágenes de la carpeta y subcarpetas que se pongan en el último ruta_carpeta_entrenamiento_def
# El código funciona entero pero hay un par de cosas que tengo que borrar porque no hacen nada, como resize_image2




import numpy as np
import os
import cv2

# Guarda en variable_destino el path de todos los elementos que se encuentren dentro de la carpeta y subcarpetas
# de ruta_carpeta que tengan la extensión dada
def guardar_elementos_de_carpeta(ruta_carpeta, variable_destino, extension):
    for carpeta_raiz, _, archivos in os.walk(ruta_carpeta):
        for nombre_archivo in archivos:
            if nombre_archivo.endswith(extension):
                ruta_imagen = os.path.join(carpeta_raiz, nombre_archivo)
                variable_destino.append(ruta_imagen)



# Según entiendo lo que tengo que hacer es primero reduzco el tamaño de las imágenes a un 25% del actual y luego 
# en base a las anotaciones vuelvo a generar las máscaras de ground truth



import cv2
import numpy as np
"""
def resize_image(image_array): #max_size=512

    # Obtener las dimensiones originales de la imagen
    height, width = image_array.shape[:2]

    """

"""
    # Calcular la relación de escala
    if height > width:
        scale = max_size / height
    else:
        scale = max_size / width
    """

"""
    scale = 0.25

    #print("scale: ", scale)

    # Calcular las nuevas dimensiones
    new_width = int(width * scale)

    #print("new_width: ", new_width)

    new_height = int(height * scale)

    #print("new_height: ", new_height)

    # Redimensionar la imagen utilizando la interpolación bicúbica
    resized_image_array = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    
    return resized_image_array

# Ejemplo de uso
# Cargar una imagen como array de NumPy
image_path = "C:/Users/MSI/OneDrive/Escritorio/Trabajo_TFG_local/TFG/TFG-IHC-Iago_Barcon_Pineiro/python/pruebas/prueba_reescalar.jpg"
image_array = cv2.imread(image_path)

# Redimensionar la imagen
resized_image = resize_image(image_array) # Funciona, ahora hay que modificar un poco el código para que no se pare en
                                                        # 512 si fuera necesario que la imagen sea más grande

path_reescalado = "C:/Users/MSI/OneDrive/Escritorio/Trabajo_TFG_local/TFG/TFG-IHC-Iago_Barcon_Pineiro/python/pruebas/prueba_reescalar_reescalada.jpg"

"""

#cv2.imwrite(url, color_seg)

#cv2.imwrite(path_reescalado, resized_image)


""" """
# Mostrar la imagen redimensionada
#cv2.imshow('Resized Image', resized_image)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


""" 
ruta_carpeta_entrenamiento_def = '../Imagenes_entrenamiento/'
path_resultado = []

extension = '.jpg'

def obtener_elemento_derecha(cadena, token):
    partes = cadena.rsplit(token, 1)
    return partes[-1]



path_resultado = ["C:/Users/MSI/OneDrive/Escritorio/Trabajo_TFG_local/TFG/TFG-IHC-Iago_Barcon_Pineiro/python/pruebas/prueba_reescalar.jpg"]

path_resultado = ["pruebas/prueba_reescalar.jpg"]

"""









""" 
# Reescalado de las imágenes de entrenamiento y validación
ruta_carpeta_entrenamiento_def = '../Imagenes_entrenamiento/'   # '../Imagenes_entrenamiento/'   '../Imagenes_validacion/'
path_resultado = []

extension = '.jpg'

guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, path_resultado, extension)

from generate_seg_mask import obtener_izquierda_delimitador

for archivos in path_resultado:

    #print("archivos: ", archivos)

    image_array = cv2.imread(archivos)

    resized_image = resize_image(image_array) # Uso la mía modificada para escala = 0.25

    nombre_archivo = obtener_izquierda_delimitador(archivos, '.')

    path_completo_sin_extension = nombre_archivo

    #token = "/"

    #nombre_archivo = obtener_elemento_derecha(path_completo_sin_extension, token)

    # Coger el nombre del archivo sin la extensión y ponerle _reescalado.png al final

    #path_archivo_reescalado2 = "reescalado/" + path_completo_sin_extension + "_reescalado2.jpg"

    path_archivo_reescalado2 = nombre_archivo + "_reescalado.jpg"

    #print("path_archivo_reescalado2: ", path_archivo_reescalado2)

    #cv2.imwrite(path_archivo_reescalado2, resized_image)


print("Fin del reescalado de las imágenes de entrenamiento o validación")
"""


""" """
import cv2
import numpy as np

def resize_image_and_mask(image_array, mask_array): #max_size=512
    # Obtener las dimensiones originales de la imagen
    height, width = image_array.shape[:2]

    scale = 0.25

    new_width = int(width * scale)
    new_height = int(height * scale)

    # Redimensionar la imagen utilizando la interpolación bicúbica
    resized_image_array = cv2.resize(image_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC)

    resized_mask_array = cv2.resize(mask_array, (new_width, new_height), interpolation=cv2.INTER_CUBIC) # Mirar de convertirlo a enteros
    # Raquel me dijo que usara bicúbica, pero Copilot me dice que use mejor cv2.INTER_NEAREST
    
    return resized_image_array, resized_mask_array



# Reescalado de las imágenes de entrenamiento y validación
ruta_carpeta_entrenamiento_def = '../Imagenes_entrenamiento/'   # '../Imagenes_entrenamiento/'   '../Imagenes_validacion/'
path_resultado = []

extension = '.jpg'

guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, path_resultado, extension)

# Reescalado de las máscaras de ground truth
#ruta_carpeta_entrenamiento_def = '../Imagenes_entrenamiento/'   # '../Imagenes_entrenamiento/'   '../Imagenes_validacion/'
path_resultado2 = []

extension = '.npy'

guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, path_resultado2, extension)

# Crear carpeta de salida 
output_base_dir = '../reescalado/' 
if not os.path.exists(output_base_dir): 
    os.makedirs(output_base_dir)

# Mantener la estructura de subcarpetas 
for archivo in path_resultado: 
    relative_path = os.path.relpath(archivo, ruta_carpeta_entrenamiento_def) 
    output_path = os.path.join(output_base_dir, relative_path) 
    output_dir = os.path.dirname(output_path) 
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir) 
    image_array = cv2.imread(archivo) 
    # resized_image = resize_image(image_array) 
    # cv2.imwrite(output_path, resized_image)

index = 0

from generate_seg_mask import obtener_izquierda_delimitador

# print("len(path_resultado): ", len(path_resultado))

# print("len(path_resultado2): ", len(path_resultado2))

for archivos in path_resultado2:

    #print("archivos: ", archivos)

    relative_path = os.path.relpath(archivos, ruta_carpeta_entrenamiento_def) 
    output_path = os.path.join(output_base_dir, relative_path) 
    output_dir = os.path.dirname(output_path) 
    if not os.path.exists(output_dir): 
        os.makedirs(output_dir) 

    image_array = cv2.imread(path_resultado[index])

    #print("path_resultado[index]: ", path_resultado[index])

    mask_array = np.load(archivos)

    #print("archivos", archivos)

    resized_image, resized_mask = resize_image_and_mask(image_array, mask_array) # Uso la mía modificada para escala = 0.25

    nombre_archivo = obtener_izquierda_delimitador(archivos, '.')

    path_archivo_reescalado_npy = nombre_archivo + "_reescalado"

    nombre_imagen = obtener_izquierda_delimitador(path_resultado[index], '.')

    path_archivo_reescalado_image = nombre_imagen + "_reescalado" + ".jpg"

    #print("path_archivo_reescalado: ", path_archivo_reescalado)

    #print("path_archivo_reescalado2: ", path_archivo_reescalado2)

    # Me lo puso Copilot
    #np.save(path_archivo_reescalado, path_archivo_reescalado)



    #np.save(path_archivo_reescalado_npy, resized_mask, allow_pickle=True) # Mi función

    np.save(output_path, resized_mask, allow_pickle=True) # Función de Copilot

    relative_image_path = os.path.relpath(path_resultado[index], ruta_carpeta_entrenamiento_def)

    output_image_path = os.path.join(output_base_dir, relative_image_path)



    #cv2.imwrite(path_archivo_reescalado_image, resized_image) # Tengo que cambiar el nombre del path de las imágenes porque pillan
                                                            # también ground_truth en el nombre y no lo pueden tener

    cv2.imwrite(output_image_path, resized_image) # Función de Copilot

    index = index + 1

print("Fin del reescalado de las máscaras de ground truth de las imágenes de entrenamiento o validación")    