
import matplotlib
matplotlib.use('TKAgg')     #Como no se puede ver nada con Qt, he mirado en internet y con este me iría     Source: https://stackoverflow.com/questions/41994485/how-to-fix-could-not-find-or-load-the-qt-platform-plugin-windows-while-using-m

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
#import seaborn as sns   #Creo que no hace falta
import numpy as np

from random import shuffle
from PIL import Image

from pycocotools.coco import COCO



#Anotaciones_Image_1029_json.json

annFile = 'IL6_1_prueba.json'  #IL6_1_prueba.json    #IL6_1.json

coco=COCO(annFile) # funciona

category_ids = coco.getCatIds()
num_categories = len(category_ids)
#print('number of categories: ',num_categories)
#for ids in category_ids:
 #   cats = coco.loadCats(ids=ids)
  #  print(cats)


# Load images for the given ids
image_ids = coco.getImgIds()

print("Valor de len(image_ids) = ")
print(len(image_ids))
print(image_ids)

#Esta línea de abajo la tengo que cambiar para que se metan todos los valores en una lista de image_id o algo así y luego con 
# eso haría el bucle o algo
image_id = image_ids[0]  # Change this line to display a different image
image_info = coco.loadImgs(image_id)

print("\n")
print("Valores de image_info = ")
print(image_info)
print("Tipo de image_info[0] = ")
print(type(image_info[0]))
print("Nombre de image_info = ")
print(image_info[0]['file_name'])
print("\n")


annotation_ids = []
annotations = []

binaryMasks = []

#Se crean las máscaras vacías porque hay el mismo número de image_ids que de annotation_ids
for id in image_ids:
    img_info = coco.loadImgs(id)[0]
    height, width = img_info['height'], img_info['width']
    aux = np.zeros((height, width), dtype=np.uint8)
    binaryMasks.append(aux)

"""
print("Valor de len(annotation_ids) = ")
print(len(annotation_ids)) #El valor de image_ids es el mismo que el de annotation_ids
print("Valor de annotation_ids = ")
print(annotation_ids)

print("\n")
print("\n")
print("Valor de len(binaryMasks) = ")
print(len(binaryMasks))
print("Valor de binaryMasks[0] = ")
print(binaryMasks[0])


print("\n")
print("\n")
print("Valor de len(annotations) = ")
print(len(annotations)) 
print("Valor de annotations = ")
print(annotations)
"""
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



#Este trozo está encima del bucle anterior

"""
# Load annotations for the given ids
annotation_ids = coco.getAnnIds(imgIds=image_id)
annotations = coco.loadAnns(annotation_ids)
print(annotations)
print("\n")
print("\n")


# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create an empty binary mask with the same dimensions as the image
binary_mask2 = np.zeros((height, width), dtype=np.uint8)


# Iterate through the annotations and draw the binary masks
for annotation in annotations:
    segmentation = annotation['segmentation']
    mask = coco.annToMask(annotation)                #Esta es la función que me dijo Raquel de usar, la función annToMask

    # Add the mask to the binary mask
    binary_mask2 += mask



"""


#Tengo que adaptar el código para leer todos las anotaciones en base a los ids de las imágenes



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

""" 

def resize_image(image_array, max_size=512):
    # Convertir el array a una imagen PIL
    img = Image.fromarray(image_array)
    if img.mode not in ('L', 'RGB'):
        img = img.convert('L')
    img.thumbnail((max_size, max_size), Image.LANCZOS) #Image.ANTIALIAS   #Image.LANCZOS    #Image.BICUBIC 
    #Flags que generan imágenes de menor calidad: Image.BILINEAR Image.NEAREST
    # Convertir la imagen PIL redimensionada de vuelta a un array
    resized_image_array = np.array(img)
    return resized_image_array

"""


import numpy as np
from PIL import Image

def resize_image(image_array, max_size=1024):
    # Convertir el array a una imagen PIL
    img = Image.fromarray(image_array)
    
    if img.mode not in ('L', 'RGB'):
        img = img.convert('L')
    
    # Redimensionar la imagen con una tupla de tamaño máximo
    img.thumbnail((max_size, max_size), Image.LANCZOS)
    
    # Crear una nueva imagen con las dimensiones exactas, rellenar si es necesario
    new_img = Image.new(img.mode, (max_size, max_size))
    new_img.paste(img, (0, 0))
    
    # Convertir la imagen PIL redimensionada de vuelta a un array
    resized_image_array = np.array(new_img)
    return  resized_image_array
#resized_mask_array = resize_image(mask_array)


#Esto lo tengo que cambiar por la lista de las máscaras que se van generando
dir_mascara_pred = '../Imagenes_para_entrenamiento/IL6_1/Image_1029diamerter300.npy' #Image_1029diamerter300

import numpy as np

masks_pred = np.load(dir_mascara_pred) #Esto lo podría obviar

print("El tipo de masks_pred es = ")
print(type(masks_pred))
print("\n")
print("\n")

#Ya no puedo implementar nada más porque solo quedan cargar las máscaras predichas y eso lo puedo hacer ya directamente en run_cellpose

#Debería hacer el reescalado después de la función aggregated_jaccard_index, pues dicha función va
#resized_masks_true = resize_image(binaryMasks, 200) # Con 128 funciona pero los valores son una puta mierda

#Con ambos debería hacer un bucle en el que se reescalen las máscaras pero ya después de que se generen todas las máscaras
#resized_mask_pred = resize_image(masks_pred, 200) # Con 200 funciona pero me llega la RAM al límite

resized_masks_true = []
resized_mask_pred = []


""" 
for index in range(0, len(binaryMasks)):
    aux = resize_image(binaryMasks[index], 150) # Con 128 funciona pero los valores son una puta mierda
    resized_masks_true.append(aux) # Con 200 funciona pero me llega la RAM al límite
    aux = resize_image(masks_pred[index], 150) 
    resized_mask_pred.append(aux) 
"""


from cellpose.metrics import aggregated_jaccard_index

resized_mask_true_aux = []
resized_mask_true_aux.append(binaryMasks[0])

resized_mask_pred_aux = []
resized_mask_pred_aux.append(masks_pred[0])

print("Tipo de resized_mask_true_aux = ")
print(type(resized_mask_true_aux))

print("Tipo de resized_mask_pred_aux = ")
print(type(resized_mask_pred_aux))

resultado = aggregated_jaccard_index(resized_mask_true_aux, resized_mask_pred_aux)
#resultado = aggregated_jaccard_index(binary_mask_single_channel, masks_pred)   #binary_mask2
#resultado = aggregated_jaccard_index(binary_mask2, masks_pred)      #Este en principio parece que da algo, en principio debería ser binary_mask pero como estoy haciendo pruebas pues ahora es con el 2
#Según he mirado parece que lo que da lo da bien pues debe dar 0 para el valor del fondo y algo cercano a 1 donde se superpongan ambas máscaras

#resultado = aggregated_jaccard_index(masks_true2, masks_pred)


print("Resultado de aggregated_jaccard_index = ")
print(resultado)
print("Tipo de \"resultado\" de aggregated_jaccard_index = ")
print(type(resultado))

#valores_positivos = np.where(resultado > 0)    #Sospecho que esto no vale para nada
#print("Resultado de aggregated_jaccard_index (valores positivos) = ")
#print(valores_positivos)

prueba_lista = []

prueba_lista.append(1)

#prueba_lista.append(num_categories)    #num_categories viene de más arriba del código copiado
                                            #Creo que es 4, una locura


#Esto lo tendría que cambiar para que fuera un bucle que recorriera todas las máscaras, las reescalara y las metiera en las listas
prueba_list_mask_true = []
#prueba_list_mask_true.append(binary_mask2)
prueba_list_mask_true.append(resized_masks_true)

prueba_list_mask_pred = []
#prueba_list_mask_pred.append(masks_pred)
prueba_list_mask_pred.append(resized_mask_pred)


from cellpose.metrics import boundary_scores

def process_in_batches(masks_true, masks_pred, batch_size):
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

import gc

gc.collect() # Forzar la recolección de basura

batch_size = 100  # Ajusta el tamaño del lote según tu memoria disponible

"""
precision, recall, fscore = process_in_batches(prueba_list_mask_true, prueba_list_mask_pred, batch_size)

#precision, recall, fscore = boundary_scores(prueba_list_mask_true, prueba_list_mask_pred, prueba_lista)
#precision, recall, fscore = boundary_scores(resized_masks_true, resized_mask_pred, prueba_lista)

#precision, recall, fscore = boundary_scores(resized_masks_true, resized_masks_pred, prueba_lista) #Probar lo del procesamiento por lotes que me dijo Copilot
#precision, recall, fscore = boundary_scores(binary_mask2, masks_pred, prueba_lista)
#precision, recall, fscore = boundary_scores(masks_true, masks_pred, 1)

#print(f"Precisión de boundary_scores = :{precision:.4f}")
print("precision de boundary_scores = ")
print(precision)
print("Tipo de \"precision\" de boundary_scores = ")
print(type(precision))

#print(f"Recall de boundary_scores = :{recall:.4f}")
print("recall de boundary_scores = ")
print(recall)
print("Tipo de \"recall\" de boundary_scores = ")
print(type(recall))

#print(f"Fscore de boundary_scores = :{fscore:.4f}")
print("fscore de boundary_scores = ")
print(fscore)
print("Tipo de \"fscore\" de boundary_scores = ")
print(type(fscore))


#print(f"Intersection over Union (IoU): {iou:.4f}")

"""
#Hago aquí el resize
resized_mask_true_aux = []
#resize_image(binaryMasks[index], 150)
resized_mask_true_aux.append(resize_image(binaryMasks[0], 256)) #binaryMasks[0]

resized_mask_pred_aux = []
#resize_image(masks_pred[index], 150)
resized_mask_pred_aux.append(resize_image(masks_pred[0], 256)) #masks_pred[0]

#precision, recall, fscore = process_in_batches(resized_mask_true_aux, resized_mask_pred_aux, batch_size)

precision, recall, fscore = boundary_scores(resized_mask_true_aux, resized_mask_pred_aux, prueba_lista)

#Volver a hacer que se lea solo el archivo Anotaciones_Image_1029_json.json para poder hacer las pruebas
#Crear y guardar en un json el diccionario con los datos de las métricas

import json

data = {}

#Función para crear el nombre del archivo donde se guardan las métricas de la imagen
def create_name_metrics_archive(full_name_metrics_archive):
    path_folder_metrics = '../Resultado_metricas/'
    full_path = path_folder_metrics + full_name_metrics_archive
    return full_path

""" Función original, funciona perfectamente

# Abrir (o crear) un archivo JSON en modo de escritura
with open('Image_1029diamerter300.json', 'w') as file:
    # Escribir el diccionario vacío en el archivo
    json.dump(data, file)

    """

def obtain_image_name(index):
    #Estas son las líneas de más arriba de donde sale la variable image_ids
    from pycocotools.coco import COCO
    annFile = 'IL6_1_prueba.json' 
    coco=COCO(annFile) 
    image_ids = coco.getImgIds()
    image_id = image_ids[index]  
    image_info = coco.loadImgs(image_id)
    nombre_imagen = image_info[0]['file_name']
    from generate_seg_mask import obtener_izquierda_delimitador
    delim = "."
    nombre_imagen_sin_extension = obtener_izquierda_delimitador(nombre_imagen, delim)
    archivo_json = nombre_imagen_sin_extension + ".json"
    return archivo_json

nombre_imagen = obtain_image_name(0)

path_metricas = create_name_metrics_archive(nombre_imagen) #'Image_1029diamerter300.json'

# Abrir (o crear) un archivo JSON en modo de escritura
with open(path_metricas, 'w') as file:  # create_name_metrics_archive('Image_1029diamerter300.json')
    # Escribir el diccionario vacío en el archivo 
    json.dump(data, file)

print("Archivo JSON vacío creado exitosamente.")

data['jaccard'] = resultado

data['precision'] = precision
data['recall'] = recall
data['fscore'] = fscore

data_serializable = {k: v.tolist() if isinstance(v, np.ndarray) else v for k, v in data.items()}

"""Función original, funciona perfectamente

with open('Image_1029diamerter300.json', 'w') as file:
    # Escribir el diccionario vacío en el archivo
    json.dump(data_serializable, file)

"""

with open(path_metricas, 'w') as file:
    # Escribir el diccionario vacío en el archivo
    json.dump(data_serializable, file)

print("Al archivo JSON se le han agregado datos")





exit()


