
import os, gc
import json
from pycocotools.coco import COCO
from pathlib import Path
from utils import obter_lista_ficheiros, es_numero, es_alfanumerico_o_guion_bajo, natural_sort_key
from parametros_HSV_RGB_LAB_de_imagenes import obtener_datos_RGB_normalizados_de_imagenes_distancias
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix


# Ya no se usa porque se ha empleado el modelo ResNet para la clasificación de la tinción de las células

# Puede haber problemas si las categorías de las tinciones anotadas manualmenteno están en el rango de 1 a 4

# Directorios
path_folder_metrics = '../../resultados/clasificacion_tincion/'


# Función para procesar archivos
def procesar_archivo(ruta):
    with open(ruta, 'r') as f:
        data = json.load(f)
    return {
        "archivo": os.path.basename(ruta),
        "tincion": data["nivel_tincion"]
    }


def obtener_directorios(ruta):
    try:
        elementos = os.listdir(ruta)
        directorios = [
            elemento for elemento in elementos 
            if os.path.isdir(os.path.join(ruta, elemento))
        ]
        directorios_ordenados = sorted(directorios, key=natural_sort_key)
        return directorios_ordenados
    except FileNotFoundError:
        print(f"La ruta especificada no existe: {ruta}")
        exit()
        return []


archivo_json = '../../config/umbrales_tincion.json'

archivo_abierto = open(archivo_json)

nombre_dir_imagenes_y_mascaras = "dir_imagenes_y_mascaras"

nombre_dir_ground_truth_general = "dir_ground_truth_general"

nombre_threshold_zscore = "threshold_no_tincion"

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
    dir_imagenes_y_mascaras = texto_valor_dir_imagenes
else:
    if(Path(texto_valor_dir_imagenes).exists() and Path(texto_valor_dir_imagenes).is_dir()):
        dir_imagenes_y_mascaras = texto_valor_dir_imagenes 
    else:
        print("Error, el valor introducido para el directorio de imágenes y máscaras no es válido")
        exit()


# Se debe pasar un directorio general de ground truth, que contenga subdirectorios con las anotaciones COCO cuyos nombres coincidan con los de las carpetas de imágenes
texto_valor_dir_ground_truth_general = valores_parametros_modelo[nombre_dir_ground_truth_general]

if(Path(texto_valor_dir_ground_truth_general).exists() and Path(texto_valor_dir_ground_truth_general).is_dir()):
    dir_ground_truth_general = texto_valor_dir_ground_truth_general 
else:
    print("Error, el valor introducido para el directorio de archivos ground_truth no es válido")
    exit()


texto_valor_threshold_zscore = valores_parametros_modelo[nombre_threshold_zscore]

if((isinstance(texto_valor_threshold_zscore, float) or isinstance(texto_valor_threshold_zscore, int)) or es_numero(texto_valor_threshold_zscore)):
    threshold_no_tincion = float(texto_valor_threshold_zscore)
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


imagenes = []
mascaras = []

for directorio in dir_imagenes_y_mascaras:
    imagenes.extend(obter_lista_ficheiros(directorio, ".jpg"))
    mascaras.extend(obter_lista_ficheiros(directorio, ".npy"))

dir_archivos = ""

gc.collect()


try:
    dir_archivos = obtener_datos_RGB_normalizados_de_imagenes_distancias(imagenes, mascaras, threshold_no_tincion, threshold_min, 
                                                          threshold_max, threshold_max_area)
    pass
except Exception as e:
    print(f"Error en obtener_datos_HSV: {e}")
    exit()

lista_directorios = obtener_directorios(dir_archivos)

valores_tincion_predichos = []
valores_tincion_ground_truth = []

for directorio in lista_directorios:
    # Directorio de anotaciones COCO correspondiente
    dir_anotaciones = os.path.join(dir_ground_truth_general, directorio)
    archivos_anotaciones = obter_lista_ficheiros(dir_anotaciones, ".json")
    
    if not archivos_anotaciones:
        print(f"No se encontraron anotaciones en el directorio: {dir_anotaciones}")
        continue

    # Cargar datos COCO
    coco = COCO(archivos_anotaciones[0])
    
    # Obtener carpetas de imágenes en el directorio actual
    dir_carpeta_imagenes = os.path.join(dir_archivos, directorio)
    carpetas_imagenes = obtener_directorios(dir_carpeta_imagenes)
    
    # Procesar cada imagen en COCO
    image_ids = coco.getImgIds()
    for image_id in image_ids:
        image_info = coco.loadImgs(image_id)
        if not image_info:
            print(f"Error al cargar información de la imagen con ID {image_id}")
            continue
        image_info = image_info[0]
        
        # Obtener el nombre base de la imagen sin extensión
        image_name_base = os.path.splitext(image_info['file_name'])[0]
        
        # Verificar si la carpeta de la imagen existe
        if image_name_base not in carpetas_imagenes:
            print(f"Advertencia: La carpeta '{image_name_base}' no existe en '{dir_carpeta_imagenes}'")
            continue
        
        # Ruta a los archivos de células
        ruta_carpeta_imagen = os.path.join(dir_carpeta_imagenes, image_name_base)
        archivos_celulas = obter_lista_ficheiros(ruta_carpeta_imagen, ".json")
        
        if not archivos_celulas:
            print(f"No se encontraron archivos de células en la carpeta: {ruta_carpeta_imagen}")
            continue
        
        # Ordenar archivos de células
        archivos_celulas_ordenados = sorted(archivos_celulas, key=natural_sort_key)
        
        # Obtener valores predichos desde archivos JSON
        valores_predichos = []
        for archivo_celula in archivos_celulas_ordenados:
            diccionario_celula = procesar_archivo(archivo_celula)
            if 'tincion' in diccionario_celula:
                valores_predichos.append(diccionario_celula['tincion'])

        # Obtener anotaciones ground truth desde COCO
        ann_ids = coco.getAnnIds(imgIds=image_id)
        annotations = coco.loadAnns(ann_ids)
        valores_ground_truth = [ann['category_id'] for ann in annotations if 'category_id' in ann]
        
        # Comparar longitudes y rellenar con -1 si es necesario
        if len(valores_predichos) != len(valores_ground_truth):
            
            if len(valores_predichos) < len(valores_ground_truth):
                print(f"La longitud de valores predichos es menor que la de ground truth para la imagen '{image_name_base}' en el directorio '{directorio}'")
            elif len(valores_predichos) > len(valores_ground_truth):
                print(f"La longitud de valores predichos es mayor que la de ground truth para la imagen '{image_name_base}' en el directorio '{directorio}'")
            print(f"Advertencia: Longitudes no coinciden para la imagen '{image_name_base}' en el directorio '{directorio}'")
            print("Longitud de valores predichos:", len(valores_predichos))
            print("Longitud de valores ground truth:", len(valores_ground_truth))
            
            # Rellenar con -1 en la lista más corta
            max_len = max(len(valores_predichos), len(valores_ground_truth))
            valores_predichos += [-1] * (max_len - len(valores_predichos))
            valores_ground_truth += [-1] * (max_len - len(valores_ground_truth))
        
        # Agregar valores a las listas principales
        valores_tincion_predichos.extend(valores_predichos)
        valores_tincion_ground_truth.extend(valores_ground_truth)

    gc.collect()


# Filtrar pares donde ambos valores sean válidos (sin -1) ya que solo perjudicarán a las métricas
pares_validos = [
    (y_true, y_pred) 
    for y_true, y_pred in zip(valores_tincion_ground_truth, valores_tincion_predichos) 
    if y_true != -1 and y_pred != -1
]

# Separar los valores filtrados
y_true_filtrado = [pair[0] for pair in pares_validos]
y_pred_filtrado = [pair[1] for pair in pares_validos]

precision = precision_score(y_true_filtrado, y_pred_filtrado, average='weighted')
recall = recall_score(y_true_filtrado, y_pred_filtrado, average='weighted')
f1 = f1_score(y_true_filtrado, y_pred_filtrado, average='weighted')
accuracy = accuracy_score(y_true_filtrado, y_pred_filtrado)
matriz_confusion = confusion_matrix(y_true_filtrado, y_pred_filtrado, labels=[1, 2, 3, 4])

# Imprimir la matriz de confusión
print("Matriz de confusión:")
print(matriz_confusion)


# Si acaso mirar de añadir otra línea con los valores de la media usando micro
diccionario_tincion = {
    "precision": precision,
    "recall": recall,
    "f1_score": f1,
    "accuracy": accuracy,
    "confusion_matrix": matriz_confusion.tolist()  # Convertir a lista para serializar en JSON
}

# Crea el directorio y subdirectorios si no existen
os.makedirs(path_folder_metrics, exist_ok=True)  

archivo_json = archivo_resultante + ".json"

# Combinar directorio y nombre del archivo
ruta_completa = os.path.join(path_folder_metrics, archivo_json)

# Guardar el diccionario en el archivo JSON
with open(ruta_completa, 'w') as archivo:
    json.dump(diccionario_tincion, archivo, indent=4)  

print(f"Archivo de métricas guardado en: {ruta_completa}")


exit()
