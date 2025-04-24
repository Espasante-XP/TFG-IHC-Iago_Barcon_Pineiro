
from pycocotools.coco import COCO
from collections import defaultdict
from utils import obter_lista_ficheiros
import os, shutil, gc


# para clasificar las células de CLAHE y HSV_normalizado hay que modificar los valores de la lista 
# carpeta_datos y cambiar HSV por el que se desee


carpetas_clasificacion = ["sin tincion", "minima", "media", "maxima"]

carpetas_datos = ["HSV", "RGB", "LAB"]

dir_general = "../../valores_comp_conexas/"

dir_nuevo_general = "../../valores_clasif_tincion"

dir_anotaciones_coco_general = "./anotaciones_coco_v2"


def obtener_indices_por_categoria(fuentes):
    """
    Devuelve índices de anotaciones agrupados por category_id y el conjunto completo de anotaciones.
    
    Args:
        fuentes (str/list): Ruta(s) a archivo(s) JSON o lista(s) de anotaciones.
        
    Returns:
        tuple: 
            - Lista de category_id únicos ordenados
            - Lista de listas de índices (posiciones) en el conjunto combinado
            - Lista de todas las anotaciones combinadas
    """
    combined_annotations = []
    
    # Convertir entrada en lista si es un solo elemento
    if not isinstance(fuentes, list):
        fuentes = [fuentes]
    
    # Cargar todas las anotaciones
    for fuente in fuentes:
        if isinstance(fuente, str):
            coco = COCO(fuente)
            combined_annotations.extend(coco.dataset['annotations'])
        elif isinstance(fuente, list):
            combined_annotations.extend(fuente)
        else:
            raise TypeError(f"Tipo no soportado: {type(fuente)}")
    
    # Crear grupos de índices por categoría
    groups = defaultdict(list)
    for idx, ann in enumerate(combined_annotations):
        groups[ann['category_id']].append(idx)
    
    # Preparar resultados ordenados
    category_ids = sorted(groups.keys())
    indices_per_category = [groups[cat_id] for cat_id in category_ids]
    
    return category_ids, indices_per_category, combined_annotations


# Se coje el directorio HSV porque es el más cómodo, pero se puede utilizar cualquiera de los 3, la estructura es la misma
dir_HSV = os.path.join(dir_general, carpetas_datos[0])

lista_carpetas = []

# Obtengo la lista de carpetas de imagenes -> Control_negativo_1', 'Control_negativo_2' ...
for carpeta in os.listdir(dir_HSV):
    if os.path.isdir(os.path.join(dir_HSV, carpeta)):
        lista_carpetas.append(carpeta)


lista_anotaciones_coco = []

# Obtengo la lista de anotaciones COCO de cada carpeta de imagenes
for directorio in lista_carpetas:
    aux = os.path.join(dir_anotaciones_coco_general, directorio)
    lista_anotaciones_coco.append(obter_lista_ficheiros(aux, ".json"))


# Lista con los 3 directorios de datos de las componentes conexas
lista_dir_datos = []

for dir in carpetas_datos:
    lista_dir_datos.append(os.path.join(dir_general, dir))


# Lista con los 12 directorios de datos de las tinciones, 4 por cada tipo de componente conexa (HSV, RGB y LAB)
# ../../valores_clasif_tincion/HSV/sin tincion, ./../valores_clasif_tincion/HSV/minima, ./../valores_clasif_tincion/HSV/media, etc
lista_dir_nuevos_datos = []

for dir in carpetas_clasificacion:
    for dir_datos in carpetas_datos:
        lista_dir_nuevos_datos.append(os.path.join(dir_nuevo_general, dir_datos, dir))


for dir_nuevo in lista_dir_nuevos_datos:
        if not os.path.exists(dir_nuevo):
            os.makedirs(dir_nuevo) # Mirar de poner el flag de que si no existe se cree para que sea más eficiente


gc.collect() 

pos_anotacion = 0
for anotaciones_coco in lista_anotaciones_coco:
    
    directorio_datos = []

    for dir_datos in lista_dir_datos:
        directorio_datos.append(os.path.join(dir_datos, lista_carpetas[pos_anotacion]))

    lista_archivos_json = []

    for dir_datos in directorio_datos:
        lista_archivos_json.append(obter_lista_ficheiros(dir_datos, ".json"))

    # Obtener índices por categoría (debe devolver 4 grupos)
    _, lista_indices, _ = obtener_indices_por_categoria(anotaciones_coco)
    
    # Validar que hay 4 categorías (tengo que darle una vuelta)
    if len(lista_indices) != 4: 
        raise ValueError(f"Se esperaban 4 categorías, pero se encontraron {len(lista_indices)} en {anotaciones_coco}")
    
    
    # Procesar cada categoría (sin anidar con tipos de datos)
    lista_archivos_categoria = []
    for categoria_idx, indices in enumerate(lista_indices):
        # Recoger archivos de todos los tipos (HSV, RGB, LAB)
        archivos_por_tipo = []
        for archivos_json in lista_archivos_json:
            # Verificar índices para este tipo de datos
            archivos_validos = []
            for idx in indices:
                if idx < len(archivos_json):
                    archivos_validos.append(archivos_json[idx]) 
                else: # Por algún motivo en Control_negativo_3 sale un index out of range 2 veces cuando no debería
                    print("len(archivos_json): ", len(archivos_json))
                    print(f"Índice {idx} fuera de rango en {os.path.dirname(archivos_json[idx-2])}") 
            archivos_por_tipo.append(archivos_validos)
        
        # Agregar a la categoría actual
        lista_archivos_categoria.append(archivos_por_tipo)


    # Modificación en la sección de copia de archivos
    for categoria_idx, categoria in enumerate(lista_archivos_categoria):
        for tipo_idx, archivos in enumerate(categoria):
            tipo_dato = carpetas_datos[tipo_idx]
            for archivo in archivos:
                # Obtener rutas de carpetas originales
                ruta_completa = os.path.dirname(archivo)
                carpeta_imagen = os.path.basename(ruta_completa)  # Ej: 'Imagen_11'
                carpeta_grupo = os.path.basename(os.path.dirname(ruta_completa))  # Ej: 'carpeta_grupo_imagenes7'
                
                # Construir ruta destino
                dir_destino = os.path.join(
                    dir_nuevo_general,
                    tipo_dato,
                    carpetas_clasificacion[categoria_idx],
                    carpeta_grupo,    # ← Carpeta del grupo (ej: carpeta_grupo_imagenes7)
                    carpeta_imagen    # ← Carpeta de la imagen (ej: Imagen_11)
                )
                
                # Crear estructura y copiar
                os.makedirs(dir_destino, exist_ok=True)
                shutil.copy(archivo, os.path.join(dir_destino, os.path.basename(archivo)))

    pos_anotacion = pos_anotacion + 1
    gc.collect() 
