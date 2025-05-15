print("Ejecutando versión actualizada del script")


"""
import os, json, gc
from utils import obter_lista_ficheiros


dir_ground_truth = "../../valores_clasif_tincion/HSV/"

dir_archivos = "../../parametros_HSV_RGB_LAB/HSV/"

path_folder_metrics = '../../resultados/clasificacion_tincion/'

tincion_por_imagen_ground_truth = []
tincion_por_imagenes_a_comparar = []

aciertos = 0
fallos = 0

sin_tincion_abs = 0
minima_abs = 0
media_abs = 0
maxima_abs = 0

sin_tincion_comparar = 0
minima_comparar = 0
media_comparar = 0
maxima_comparar = 0


def obtener_tincion_de_lista_archivos(lista_archivos, nombre_archivo):
    for archivo in lista_archivos:
        if archivo['archivo'] == nombre_archivo:
            return archivo['tincion']
    return None


archivos_ground_truth = obter_lista_ficheiros(dir_ground_truth, ".json")

archivos_a_comparar = obter_lista_ficheiros(dir_archivos, ".json")


print("len(archivos_a_comparar): ", len(archivos_a_comparar))

print("len(archivos_ground_truth): ", len(archivos_ground_truth))

print("Se comienza a procesar los archivos de comparación")

for archivo in archivos_ground_truth: 

    #print("index: ", index)
    #print("archivo: ", archivo)
    # Cargar el archivo JSON
    with open(archivo, 'r') as f:
        data = json.load(f)

    # Obetner el nombre del archivo
    nombre_archivo = os.path.basename(archivo)

    # Obtener la lista de imágenes
    nivel_tincion = data['nivel_tincion']           

    # Crear diccionario para almacenar la tinción por archivo
    archivo_y_tincion = {
        'archivo': nombre_archivo,
        'tincion': nivel_tincion
    }

    # Agregar el diccionario a la lista
    tincion_por_imagen_ground_truth.append(archivo_y_tincion)


print("len(tincion_por_imagen_ground_truth): ", len(tincion_por_imagen_ground_truth))

nombre = "Image_1134_cell_1.json"

for archivo_tincion in tincion_por_imagen_ground_truth:
    if archivo_tincion['archivo'] == nombre:
        print(f"Nivel de tinción para {nombre}: {archivo_tincion['tincion']}")
        break


for archivo in archivos_a_comparar: 

    #print("index: ", index)
    #print("archivo: ", archivo)
    # Cargar el archivo JSON
    with open(archivo, 'r') as f:
        data = json.load(f)

    # Obetner el nombre del archivo
    nombre_archivo = os.path.basename(archivo)

    # Obtener la lista de imágenes
    nivel_tincion = data['nivel_tincion']

    # Crear diccionario para almacenar la tinción por archivo
    archivo_y_tincion = {
        'archivo': nombre_archivo,
        'tincion': nivel_tincion
    }

    # Agregar el diccionario a la lista
    tincion_por_imagenes_a_comparar.append(archivo_y_tincion)

# obtener_tincion_de_lista_archivos(lista_archivos, nombre_archivo)

gc.collect()

index = 0
for archivo_tincion in tincion_por_imagenes_a_comparar:
    index = index + 1

    tincion_ground_truth = obtener_tincion_de_lista_archivos(tincion_por_imagen_ground_truth, archivo_tincion['archivo'])

    if tincion_ground_truth is None:
        print(f"Archivo {archivo_tincion['archivo']} no encontrado en ground truth")
        continue

    tincion_a_comparar = archivo_tincion['tincion']

    if tincion_ground_truth == "sin tincion":
        sin_tincion_abs += 1
    elif tincion_ground_truth == "minima":
        minima_abs += 1
    elif tincion_ground_truth == "media":
        media_abs += 1
    elif tincion_ground_truth == "maxima":
        maxima_abs += 1 

    if tincion_a_comparar == "sin tincion":
        sin_tincion_comparar += 1
    elif tincion_a_comparar == "minima":
        minima_comparar += 1
    elif tincion_a_comparar == "media":
        media_comparar += 1
    elif tincion_a_comparar == "maxima":
        maxima_comparar += 1 

    if tincion_ground_truth == tincion_a_comparar:
        aciertos += 1
    else:
        fallos += 1


print(f"Se realizan {index} iteraciones del bucle")

porcentaje_aciertos = (aciertos / len(tincion_por_imagenes_a_comparar)) * 100

print("Aciertos: ", aciertos)
print("Fallos: ", fallos)

print("Aciertos + Fallos: ", aciertos + fallos)
print("Total de imágenes comparadas: ", len(tincion_por_imagenes_a_comparar))

print("")
print("")

print("Porcentaje de aciertos: ", porcentaje_aciertos)

print("sin_tincion_abs: ", sin_tincion_abs)
print("sin_tincion_comparar: ", sin_tincion_comparar)

print("minima_abs: ", minima_abs)
print("minima_comparar: ", minima_comparar)

print("media_abs: ", media_abs)
print("media_comparar: ", media_comparar)

print("maxima_abs: ", maxima_abs)
print("maxima_comparar: ", maxima_comparar)


diccionario_tincion = {
    "aciertos": aciertos,
    "fallos": fallos,
    "sin tincion": {
        "ground_truth": sin_tincion_abs,
        "comparar": sin_tincion_comparar
    },
    "minima": {
        "ground_truth": minima_abs,
        "comparar": minima_comparar
    },
    "media": {
        "ground_truth": media_abs,
        "comparar": media_comparar
    },
    "maxima": {
        "ground_truth": maxima_abs,
        "comparar": maxima_comparar
    },
    "porcentaje aciertos": porcentaje_aciertos
}

#path_dir = "../"  # Directorio donde se guardará el archivo
nombre_archivo = "metricas_clasificacion_tincion.json"  # Nombre del archivo JSON

# 3. Crear el directorio si no existe
os.makedirs(path_folder_metrics, exist_ok=True)  # Crea el directorio y subdirectorios si no existen

# 4. Combinar directorio y nombre del archivo
ruta_completa = os.path.join(path_folder_metrics, nombre_archivo)  # Combina ambas partes de la ruta

# 5. Guardar el diccionario en el archivo JSON
with open(ruta_completa, 'w') as archivo:
    json.dump(diccionario_tincion, archivo, indent=4)  # indent=4 mejora la legibilidad del JSON 

print(f"Archivo guardado en: {ruta_completa}")
"""


""" Idea original para la comparación usando el bucle for
index = 0
for archivo_tincion in tincion_por_imagenes_a_comparar:
    index = index + 1
    for archivo_ground_truth in tincion_por_imagen_ground_truth: # Este bucle me lo podría saltar si usara el diccionario
        if archivo_ground_truth['archivo'] == archivo_tincion['archivo']:

            tincion_ground_truth = archivo_ground_truth['tincion']
            tincion_a_comparar = archivo_tincion['tincion']

            if tincion_ground_truth == "sin tincion":
                sin_tincion_abs += 1
            elif tincion_ground_truth == "minima":
                minima_abs += 1
            elif tincion_ground_truth == "media":
                media_abs += 1
            elif tincion_ground_truth == "maxima":
                maxima_abs += 1 

            if tincion_a_comparar == "sin tincion":
                sin_tincion_comparar += 1
            elif tincion_a_comparar == "minima":
                minima_comparar += 1
            elif tincion_a_comparar == "media":
                media_comparar += 1
            elif tincion_a_comparar == "maxima":
                maxima_comparar += 1 

            if tincion_ground_truth == tincion_a_comparar:
                aciertos += 1
            else:
                fallos += 1
"""





"""
# Versión con hilos, para acceder a los archivos es una cosa

import os
import json
from concurrent.futures import ThreadPoolExecutor
from utils import obter_lista_ficheiros

dir_ground_truth = "../../valores_clasif_tincion/HSV/"

# Función que procesa un solo archivo
def procesar_archivo(archivo):
    with open(archivo, 'r') as f:
        data = json.load(f)
    nombre_archivo = os.path.basename(archivo)
    nivel_tincion = data['nivel_tincion']
    return {'archivo': nombre_archivo, 'tincion': nivel_tincion}

# Obtener lista de archivos
archivos_ground_truth = obter_lista_ficheiros(dir_ground_truth, ".json")
print("len(archivos_ground_truth): ", len(archivos_ground_truth))
print("Se comienza a procesar los archivos de comparación")

# Procesar archivos en paralelo con hilos
with ThreadPoolExecutor(max_workers=8) as executor:  # Ajusta max_workers según tu sistema
    resultados = list(executor.map(procesar_archivo, archivos_ground_truth))

print("len(resultados): ", len(resultados))


# Obtener valores de tinción por archivo directamente
nombre_buscado = "Image_995_cell_1.json"
resultado = next((item for item in resultados if item['archivo'] == nombre_buscado), None)

if resultado:
    print(f"Nivel de tinción para {nombre_buscado}: {resultado['tincion']}")
else:
    print(f"Archivo {nombre_buscado} no encontrado")

# Obtener valores de tinción por archivo transformando la lista de resultados a un diccionario (creo que es más claro de entender)   
resultados_dict = {item['archivo']: item['tincion'] for item in resultados}
nombre_buscado = "Image_995_cell_1.json"

tincion = resultados_dict.get(nombre_buscado)
if tincion is not None:
    print(f"Nivel de tinción para {nombre_buscado}: {tincion}")
else:
    print(f"Archivo {nombre_buscado} no encontrado")

"""



import os
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from utils import obter_lista_ficheiros, es_numero, es_alfanumerico_o_guion_bajo


# Directorios
dir_ground_truth = "../../valores_clasif_tincion/HSV/" # Lo tengo en el json
dir_archivos = "../../parametros_HSV_RGB_LAB/HSV/" # Ya lo saco de la función
path_folder_metrics = '../../resultados/clasificacion_tincion/' # Lo necesito


# Función para procesar archivos
def procesar_archivo(ruta):
    with open(ruta, 'r') as f:
        data = json.load(f)
    return {
        "archivo": os.path.basename(ruta),
        "tincion": data["nivel_tincion"]
    }


archivo_json = '../../config/analisis_tincion.json'

archivo_abierto = open(archivo_json)

nombre_dir_imagenes_y_mascaras = "dir_imagenes_y_mascaras"

nombre_dir_ground_truth = "dir_ground_truth"

nombre_threshold_zscore = "threshold_zscore"

nombre_threshold_min = "threshold_min"

nombre_threshold_max = "threshold_max"

nombre_threshold_max_area = "threshold_max_area"

nombre_archivo_resultante = "archivo_resultante"

valores_parametros_modelo = json.load(archivo_abierto)


#Comprobaciones de que los valores cargados son correctos
texto_valor_dir_imagenes = valores_parametros_modelo[nombre_dir_imagenes_y_mascaras]

if(isinstance(texto_valor_dir_imagenes, list)): # Si es una lista de directorios, se comprueba que todos los directorios valgan
    for directorio in texto_valor_dir_imagenes:
        if(not Path(directorio).exists() or not Path(directorio).is_dir()):
            print("Error, el valor introducido para el directorio de imágenes y máscaras no es válido")
            exit()
    dir_imagenes_y_mascaras_hsv = texto_valor_dir_imagenes
else:
    if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
        dir_imagenes_y_mascaras_hsv = texto_valor_dir_imagenes 
    else:
        print("Error, el valor introducido para el directorio de imágenes y máscaras no es válido")
        exit()


# Está soportado que se pase una lista de directorios pero lo ideal sería que todos los archivos estuvieran en el mismo directorio
texto_valor_dir_ground_truth = valores_parametros_modelo[nombre_dir_ground_truth]

if(isinstance(texto_valor_dir_ground_truth, list)): # Si es una lista de directorios, se comprueba que todos los directorios valgan
    for directorio in texto_valor_dir_ground_truth:
        if(not Path(directorio).exists() or not Path(directorio).is_dir()):
            print("Error, el valor introducido para el directorio de archivos ground_truth no es válido")
            exit()
    dir_ground_truth = texto_valor_dir_ground_truth
else:
    if(Path(texto_valor_dir_ground_truth).exists() and Path(texto_valor_dir_ground_truth).is_dir()):
        dir_ground_truth = texto_valor_dir_ground_truth 
    else:
        print("Error, el valor introducido para el directorio de archivos ground_truth no es válido")
        exit()


texto_valor_threshold_zscore = valores_parametros_modelo[nombre_threshold_zscore]

if((isinstance(texto_valor_threshold_zscore, float) or isinstance(texto_valor_threshold_zscore, int)) or es_numero(texto_valor_threshold_zscore)):
    threshold_zscore = float(texto_valor_threshold_zscore)
else:
    print("Error, el valor introducido para el umbral de diferencia de fondo no es válido")
    exit()    


texto_valor_threshold_min = valores_parametros_modelo[nombre_threshold_min]

if(es_numero(texto_valor_threshold_min)):
    if(float(texto_valor_threshold_min) >= 0 or float(texto_valor_threshold_min) <= 100):
        threshold_min = float(texto_valor_threshold_min)
    else: 
        print("Error, el valor introducido para el umbral del porcentaje de valores de la tinción mínima no es válido")
        exit()
else:
    print("Error, el valor introducido para el umbral del porcentaje de valores de la tinción mínima no es válido")
    exit()    


texto_valor_threshold_max = valores_parametros_modelo[nombre_threshold_max]

if(es_numero(texto_valor_threshold_max)):
    if(float(texto_valor_threshold_max) < threshold_min):
        print("Error, el valor introducido para el umbral del porcentaje de valores de la tinción máxima debe ser superior al de la tinción mínima")
        exit()
    if(float(texto_valor_threshold_max) >= 0 or float(texto_valor_threshold_max) <= 100):
        threshold_max = float(texto_valor_threshold_max)
    else:
        print("Error, el valor introducido para el umbral del porcentaje de valores de la tinción máxima no es válido")
        exit()    
else:
    print("Error, el valor introducido para el umbral de diferencia de fondo no es válido")
    exit()    


texto_valor_threshold_max_area = valores_parametros_modelo[nombre_threshold_max_area]

if(es_numero(texto_valor_threshold_max_area)):
    if(float(texto_valor_threshold_max_area) < 0 or float(texto_valor_threshold_max_area) > 1):
        print("Error, el valor introducido para el umbral de la superficie tintada de la célula debe estar entre 0 y 1")
        exit()
    else:    
        threshold_max_area = float(texto_valor_threshold_max_area)
else:
    print("Error, el valor introducido para el umbral de la superficie tintada de la célula no es válido")
    exit()     


texto_valor_archivo_resultante = valores_parametros_modelo[nombre_archivo_resultante]

if(isinstance(texto_valor_archivo_resultante, str)):
    if(es_alfanumerico_o_guion_bajo(texto_valor_archivo_resultante)):
        archivo_resultante = texto_valor_archivo_resultante
    else:
        print("Error, el valor introducido para el nombre del archivo resultante no es válido")
        exit()


dir_imagenes_y_mascaras_hsv =  ["../../Imagenes_entrenamiento_reescalado", "../../Imagenes_validacion_reescalado/"]

archivo_json = archivo_resultante + ".json"

print("archivo_json: ", archivo_json)

#exit()

imagenes_hsv = []
mascaras_hsv = []

for directorio in dir_imagenes_y_mascaras_hsv:
    imagenes_hsv.extend(obter_lista_ficheiros(directorio, ".jpg"))
    mascaras_hsv.extend(obter_lista_ficheiros(directorio, ".npy"))


#threshold_zscore = 1 # 3
#threshold_min = 0.5 # 0.15
#threshold_max = 0.6
#threshold_max_area = 0.5

#exit()

print("Inicia el código")


dir_archivos = ""

from parametros_HSV_RGB_LAB_de_imagenes import obtener_datos_HSV_normalizados_de_imagenes_distancias

""""""

try:
    
    dir_archivos = obtener_datos_HSV_normalizados_de_imagenes_distancias(imagenes_hsv, mascaras_hsv, threshold_zscore, threshold_min, 
                                                          threshold_max, threshold_max_area)
    
    pass
except Exception as e:
    print(f"Error en obtener_datos_HSV: {e}")
    exit()



# Obtener listas de archivos
archivos_ground_truth = []
archivos_a_comparar = []

for dir_g_truth in dir_ground_truth:
    archivos_ground_truth.extend(obter_lista_ficheiros(dir_ground_truth, ".json"))
    
archivos_a_comparar = obter_lista_ficheiros(dir_archivos, ".json")

print(f"Total de archivos ground truth: {len(archivos_ground_truth)}")
print(f"Total de archivos a comparar: {len(archivos_a_comparar)}")
print("Iniciando procesamiento...")

# Procesar archivos ground truth en paralelo
with ThreadPoolExecutor(max_workers=8) as executor:
    resultados_gt = list(executor.map(procesar_archivo, archivos_ground_truth))

# Crear diccionario de ground truth para acceso rápido en el bucle for
ground_truth_dict = {item["archivo"]: item["tincion"] for item in resultados_gt}

# Procesar archivos a comparar en paralelo
with ThreadPoolExecutor(max_workers=6) as executor:
    lista_archivos_a_comparar = list(executor.map(procesar_archivo, archivos_a_comparar))

aciertos = 0
fallos = 0

sin_tincion_abs = 0
minima_abs = 0
media_abs = 0
maxima_abs = 0

sin_tincion_comparar = 0
minima_comparar = 0
media_comparar = 0
maxima_comparar = 0

print("Comienza la comparación de resultados")

# Comparar resultados
for item in lista_archivos_a_comparar:

    archivo = item["archivo"]
    tincion_ground_truth = ground_truth_dict.get(archivo)
    
    if tincion_ground_truth is None:
        continue  # Saltar si no hay coincidencia en ground truth
        
    tincion_a_comparar = item["tincion"]

    if tincion_ground_truth == "sin tincion":
        sin_tincion_abs += 1
    elif tincion_ground_truth == "minima":
        minima_abs += 1
    elif tincion_ground_truth == "media":
        media_abs += 1
    elif tincion_ground_truth == "maxima":
        maxima_abs += 1 

    if tincion_a_comparar == "sin tincion":
        sin_tincion_comparar += 1
    elif tincion_a_comparar == "minima":
        minima_comparar += 1
    elif tincion_a_comparar == "media":
        media_comparar += 1
    elif tincion_a_comparar == "maxima":
        maxima_comparar += 1 

    if tincion_ground_truth == tincion_a_comparar:
        aciertos += 1
    else:
        fallos += 1

    


porcentaje_aciertos = (aciertos / len(lista_archivos_a_comparar)) * 100 # len(lista_archivos_a_comparar) = aciertos + fallos



print("Aciertos: ", aciertos)
print("Fallos: ", fallos)

print("Aciertos + Fallos: ", aciertos + fallos)
print("Total de imágenes comparadas: ", len(lista_archivos_a_comparar))

print("")
print("")

print("Porcentaje de aciertos: ", porcentaje_aciertos)


print("sin_tincion_abs: ", sin_tincion_abs)
print("sin_tincion_comparar: ", sin_tincion_comparar)

dir_aux = os.path.join(dir_ground_truth, "sin tincion")

aux = obter_lista_ficheiros(dir_aux, ".json")

print("elem sin tincion: ", len(aux))

print("minima_abs: ", minima_abs)
print("minima_comparar: ", minima_comparar)

dir_aux = os.path.join(dir_ground_truth, "minima")

aux = obter_lista_ficheiros(dir_aux, ".json")

print("elem tincion minima: ", len(aux))

print("media_abs: ", media_abs)
print("media_comparar: ", media_comparar)

dir_aux = os.path.join(dir_ground_truth, "media")

aux = obter_lista_ficheiros(dir_aux, ".json")

print("elem tincion media: ", len(aux))

print("maxima_abs: ", maxima_abs)
print("maxima_comparar: ", maxima_comparar)

dir_aux = os.path.join(dir_ground_truth, "maxima")

aux = obter_lista_ficheiros(dir_aux, ".json")

print("elem tincion maxima: ", len(aux))



diccionario_tincion = {
    "aciertos": aciertos,
    "fallos": fallos,
    "sin tincion": {
        "ground_truth": sin_tincion_abs,
        "comparar": sin_tincion_comparar
    },
    "minima": {
        "ground_truth": minima_abs,
        "comparar": minima_comparar
    },
    "media": {
        "ground_truth": media_abs,
        "comparar": media_comparar
    },
    "maxima": {
        "ground_truth": maxima_abs,
        "comparar": maxima_comparar
    },
    "porcentaje aciertos": porcentaje_aciertos
}

#path_dir = "../"  # Directorio donde se guardará el archivo
nombre_archivo = "metricas_clasificacion_tincion.json"  # Nombre del archivo JSON

# 3. Crear el directorio si no existe
os.makedirs(path_folder_metrics, exist_ok=True)  # Crea el directorio y subdirectorios si no existen

archivo_json = archivo_resultante + ".json"

# 4. Combinar directorio y nombre del archivo
ruta_completa = os.path.join(path_folder_metrics, archivo_json)  # Combina ambas partes de la ruta

# 5. Guardar el diccionario en el archivo JSON
with open(ruta_completa, 'w') as archivo:
    json.dump(diccionario_tincion, archivo, indent=4)  # indent=4 mejora la legibilidad del JSON 

print(f"Archivo guardado en: {ruta_completa}")



""""""


"""
# Calcular porcentaje de aciertos
total = len(lista_archivos_a_comparar)
estadisticas["porcentaje_aciertos"] = (estadisticas["aciertos"] / total * 100) if total > 0 else 0

# Guardar resultados
os.makedirs(path_folder_metrics, exist_ok=True)
ruta_completa = os.path.join(path_folder_metrics, "metricas_clasificacion_tincion.json")

with open(ruta_completa, 'w') as f:
    json.dump(estadisticas, f, indent=4)

print(f"Proceso completado. Archivo guardado en: {ruta_completa}")
print(f"Aciertos: {estadisticas['aciertos']}, Fallos: {estadisticas['fallos']}")
print(f"Porcentaje de aciertos: {estadisticas['porcentaje_aciertos']:.2f}%")
"""



""" del final del bucle for
    # Actualizar estadísticas
    estadisticas[f"{tincion_gt}"]["ground_truth"] += 1
    estadisticas[f"{tincion_comparar}"]["comparar"] += 1
    
    if tincion_gt == tincion_comparar:
        estadisticas["aciertos"] += 1
    else:
        estadisticas["fallos"] += 1
    """