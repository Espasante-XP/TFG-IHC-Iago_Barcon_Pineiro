
import numpy as np
from pycocotools.coco import COCO
import os
import json
import cv2


def cargar_anotaciones_coco_de_archivo(annFile: os.path):
    """
    Carga anotaciones COCO y genera máscaras multietiqueta para cada imagen.

    Args:
        annFile (os.path o str): Ruta al archivo JSON de anotaciones COCO.

    Returns:
        tuple: Contiene:
            - coco (COCO): Objeto COCO inicializado.
            - mascaras_multietiqueta (list): Lista de arrays numpy con máscaras etiquetadas.
            - nombres_imagenes (list): Lista de nombres de archivo de las imágenes.
    """
    
    coco=COCO(annFile) 

    image_ids = coco.getImgIds()

    mascaras_multietiqueta = []

    informacion_imagenes = []

    #Se crean las máscaras vacías, hay tantas imágenes (image_ids) como anotaciones (annotation_ids)
    for id in image_ids:
        img_info = coco.loadImgs(id)[0]
        height, width = img_info['height'], img_info['width']
        aux = np.zeros((height, width), dtype=np.uint8)
        mascaras_multietiqueta.append(aux)
        informacion_imagenes.append(img_info)

    annotations = []
    index = 0

    for id in image_ids:
        annotation = coco.getAnnIds(imgIds=id)
        annotations = coco.loadAnns(annotation)
        for ann_index, annotation in enumerate(annotations):
            mask = coco.annToMask(annotation)                
            mascaras_multietiqueta[index][mask>0] = ann_index + 1 # Se añade 1 para que sea distinguible del fondo, el cual es 0
        index = index + 1

    nombres_imagenes = [img['file_name'] for img in informacion_imagenes]

    return coco, mascaras_multietiqueta, nombres_imagenes


def generate_coco_via_bueno(mask: np.ndarray, image_name: str, stains: list):
    """
    Genera un archivo COCO desde una máscara de segmentación y una lista de tinciones.
    Args:
        mask (np.ndarray): Máscara de segmentación con valores únicos para cada categoría.
        image_name (str): Nombre de la imagen asociada a la máscara.
        stains (list): Lista de valores de tinción correspondientes a cada categoría en la máscara.
    Returns:
        dict: Estructura de datos en formato COCO.
    """

    unique_labels = np.sort(np.unique(mask)[np.unique(mask) != 0])
    if len(stains) != len(unique_labels):
        raise ValueError("La longitud de la lista de tinciones debe coincidir con los valores únicos no cero de las máscaras.")

    if any(stain not in [1, 2, 3, 4] for stain in stains):
        raise ValueError("Los valores de la lista de tinciones deben estar entre 1 y 4 (válidos para las categorías predefinidas).")

    # Categorías predefinidas (sin tildes) porque con tildes se exporta mal a JSON
    categories = [
        {"supercategory": "tincion", "id": 1, "name": "0 - sen tincion"},
        {"supercategory": "tincion", "id": 2, "name": "1 - minima"},
        {"supercategory": "tincion", "id": 3, "name": "2 - media"},
        {"supercategory": "tincion", "id": 4, "name": "3 - maxima"}
    ]

    # Inicializar estructura de anotaciones
    annotations = []
    ann_id = 0  # Contador global de anotaciones

    # Procesar cada valor único en la máscara (sin fondo)
    for idx, label in enumerate(unique_labels):
        # Obtener el category_id desde stains
        category_id = stains[idx]

        # Máscara binaria para este valor
        binary_mask = (mask == label).astype(np.uint8)

        # Encontrar componentes conectados (cada objeto)
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary_mask, connectivity=8)

        for obj_id in range(1, num_labels):  # Saltar fondo (obj_id=0)
            # Máscara del objeto actual
            obj_mask = (labels == obj_id).astype(np.uint8)
            contours, _ = cv2.findContours(obj_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if not contours:
                continue

            # Concatenar todos los puntos y eliminar dimensiones extra
            all_points = np.concatenate(contours).reshape(-1, 2)

            # Calcular bounding box y área
            x_coords = all_points[:, 0]
            y_coords = all_points[:, 1]
            x_min, x_max = x_coords.min(), x_coords.max()
            y_min, y_max = y_coords.min(), y_coords.max()
            bbox = [int(x_min), int(y_min), int(x_max - x_min), int(y_max - y_min)]
            area = cv2.contourArea(all_points)

            # Procesar segmentación como polígono
            segmentation = []
            for contour in contours:
                flat = []
                for point in contour[:, 0]:
                    flat.extend(point.tolist())
                segmentation.append(flat)

            # Agregar anotación
            annotations.append({
                "id": ann_id,
                "image_id": 0,
                "category_id": category_id,
                "bbox": bbox,
                "segmentation": segmentation,
                "area": float(area),
                "iscrowd": 0
            })
            ann_id += 1

    # Estructura final del archivo COCO
    height, width = mask.shape
    coco_data = {
        "images": [{
            "id": 0,
            "file_name": image_name,
            "width": int(width),
            "height": int(height)
        }],
        "annotations": annotations,
        "categories": categories
    }

    return coco_data



if __name__ == "__main__":

    segmentation_mask_url = "../../Imagenes_entrenamiento/Control_negativo_1/Image_994_ground_truth.npy"

    segmentation_mask = np.load(segmentation_mask_url)
    
    array_valores_tincion = [2, 2, 2, 0, 1, 2, 1, 1, 1, 2, 0] # Los valores de tinción de cada una de las células de Image_994 de Control_negativo_1

    array_valores_tincion_1a4 = [t + 1 for t in array_valores_tincion] # Convertir los valores de tinción a 1, 2, 3, 4 (de 0, 1, 2, 3) para que sean compatibles con las categorías predefinidas

    stains = array_valores_tincion_1a4

    # Limpiar el código y subirlo para que me diga Raquel que es lo que puede estar mal
    
    nombre_imagen = "Image_994.jpg"

    data = {"name": "tinción"}
    with open("test.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

    coco_via = generate_coco_via_bueno(segmentation_mask, nombre_imagen, stains) 

    archivo_guardar = "prueba2_funcion_nueva_transform_anotaciones_via.json"

    # Guardar en archivo JSON
    with open(archivo_guardar, "w") as f:
        json.dump(coco_via, f, ensure_ascii=False)
    
    try:
        coco = COCO(archivo_guardar)
    except Exception as e:
        print(f"Error al cargar el archivo COCO: {e}")    

    exit(0)



