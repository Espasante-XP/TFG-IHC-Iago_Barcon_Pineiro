
import numpy as np

from generate_seg_mask import generate_seg_mask

imagen_mascara = '../Imagenes_para_entrenamiento/IL6_1/Image_1031_mask.png'

archivo_mascara = '../Imagenes_para_entrenamiento/IL6_1/Image_1031.npy'

imagenes = []

ruta_carpeta = '../Imagenes_para_entrenamiento/IL6_1'   #./Imagenes_para_entrenamiento/IL6_1

#C:\Users\iagob\OneDrive\Escritorio\Trabajo_TFG_local\TFG\Trabajo_TFG_actual\Imagenes para entrenamiento\IL6_1

import time, os, sys

#Prueba para hacer la impresión
for index in range(0,10):
    print(f"Valor de index = {index}")

for nombre_archivo in os.listdir(ruta_carpeta):
    # Asegúrate de poner aquí todos los formatos que quieras cargar
    if nombre_archivo.endswith('.jpg'): # or nombre_archivo.endswith('.png'): 
        #print("Entra en el bucle")
        ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
        #print(ruta_imagen)
        #imagen = Image.open(ruta_imagen)
        #print(imagen)
        #imagenes.append(imagen)
        imagenes.append(ruta_imagen)

textFile = imagenes[2]

def obtener_izquierda_delimitador(cadena, delimitador):
    # Encuentra la última ocurrencia del delimitador
    indice = cadena.rfind(delimitador)
    
    # Si el delimitador no se encuentra, devuelve la cadena completa
    if indice == -1:
        return cadena
    
    # Devuelve la parte de la cadena a la izquierda del delimitador
    return cadena[:indice]

# Ejemplo de uso
cadena = imagenes[2]

#delimitador = "/"
delimitador = "."

resultado = obtener_izquierda_delimitador(cadena, delimitador)
print(resultado)  # Salida: "esto/es/un/ejemplo/de"


# Cargar el archivo .npy como un array de numpy
mascara = np.load(archivo_mascara, allow_pickle=True) #Tengo que poner allow_pickle=True porque si no no me deja cargarlo

# Imprimir la forma del array para verificar sus dimensiones
print("máscara = ")
print(mascara.shape)

#generate_seg_mask(imagen_mascara, mascara)


#Generado por Copilot
import json

"""
# Función para obtener el valor de un nombre específico
def obtener_valor_por_nombre(archivo_json, nombre):
    with open(archivo_json, 'r') as file:
        data = json.load(file)
        for item in data:
            if item.get('nombre') == nombre:
                return item
        return "Nombre no encontrado"

        """


"""
Función para cargar archivos JSON
"""
# Nombre del archivo JSON y nombre que deseas buscar
archivo_json = '../Valores_para_evaluacion/parametros_model_eval.json'
#archivo_json = 'archivo.json'
nombre = 'diameter'

archivo_abierto = open(archivo_json)

# Obtener el valor del nombre
valores = json.load(archivo_abierto)

print("Valor de diameter en el json = ")
print(valores["diameter"])

# Imprimir el valor
#print(f"El valor de diameter '{nombre}' es: {valor}")





#import json
#import numpy as np

"""
# Cargar datos desde un archivo JSON
with open('Anotaciones_Image_1029_json.json', 'r') as file:
    data = json.load(file)
"""

"""
    Pruebas que no funcionan para usar las funciones de evaluación de las máscaras

archivo_json2 = 'Anotaciones_Image_1029_json.json'

archivo_abierto2 = open(archivo_json2)

valores = json.load(archivo_abierto2)


# Convertir los datos a un array de NumPy
numpy_array = np.array(valores)

# Guardar el array de NumPy en un archivo NPY
np.save('Anotaciones_Image_1029_json.npy', numpy_array)

#masks_true = 'IL6_1.json'

masks_true = 'Anotaciones_Image_1029_json.npy'

masks_pred = '../Imagenes_para_entrenamiento/IL6_1/Image_1029.npy'

masks_true2 = np.load(masks_true, allow_pickle=True) #Tengo que poner allow_pickle=True porque si no no me deja cargarlo

print("Shape masks_true2 = ")
print(masks_true2.shape)

print("Type masks_true2 = ")
print(type(masks_true2))

#print("Len masks_true2 = ")
#print(masks_true2.len)

#Explicación funciones de metrics: https://www.bing.com/chat?q=%C2%BFQu%C3%A9+es+Copilot%3F&showconv=1&filters=wholepagesharingscenario%3A%22Conversation%22&shareId=17d61e83-a2b3-4ec3-bd67-e1bef0822a9d&shtc=0&shth=OBFB.73FF6ADE8CC93B6ED1EDA1CE557E2E09&shsc=Codex_ConversationMode&form=EX0050&shid=9bc7692d-f065-4b8a-b65f-bf712599ae8b&shtp=GetUrl&shtk=SW5kw61jYW1lIHF1ZSBoYWNlIGNhZGEgdW5hIGRlIGxhcyBmdW5jaW9uZXMgZGVsIGFyY2hpdm8gbWV0cmljcy5weSBxdWUgc2UgZW5jdWVudHJhIGRlbnRybyBkZSBsYSBjYXJwZXRhIGNlbGxwb3NlIGRlbCByZXBvc2l0b3JpbyBjZWxscG9zZSAoaHR0cHM6Ly9naXRodWIuY29tL01vdXNlTGFuZC9jZWxscG9zZSk%3D&shdk=QXF1w60gZXN0w6EgdW5hIHJlc3B1ZXN0YSBxdWUgaGUgb2J0ZW5pZG8gY29uIE1pY3Jvc29mdCBDb3BpbG90LCBlbCBwcmltZXIgbW90b3IgZGUgcmVzcHVlc3RhcyBjb24gdGVjbm9sb2fDrWEgZGUgaW50ZWxpZ2VuY2lhIGFydGlmaWNpYWwgZGVsIG11bmRvLiBTZWxlY2Npb25lIGVzdGEgb3BjacOzbiBwYXJhIHZlciBsYSByZXNwdWVzdGEgY29tcGxldGEgbyBwcnXDqWJlbGEgdXN0ZWQgbWlzbW8u&shhk=IFVWNGa3ZT8LXE7aFVscYLiPkV4WK5l%2Bber86WzucqY%3D

#Tengo un archivo txt con explicaciones más detalladas

from cellpose.metrics import aggregated_jaccard_index

#resultado = aggregated_jaccard_index(masks_true2, masks_pred)

#resultado = aggregated_jaccard_index(numpy_array, masks_pred)

#aggregated_jaccard_index(masks_true, masks_pred)


"""

"""
Args:
        masks_true (list of np.ndarrays (int) or np.ndarray (int)): 
            where 0=NO masks; 1,2... are mask labels
        masks_pred (list of np.ndarrays (int) or np.ndarray (int)): 
            np.ndarray (int) where 0=NO masks; 1,2... are mask labels

    Returns:
        aji (float): aggregated jaccard index for each set of masks
    
"""


#from cellpose.metrics import boundary_scores

#precision, recall, fscore = boundary_scores(masks_true, masks_pred, 1)
#boundary_scores(masks_true, masks_pred, scales):

"""
    Args:
        masks_true (list): List of true masks.
        masks_pred (list): List of predicted masks.
        scales (list): List of scales.

    Returns:
        tuple: A tuple containing precision, recall, and F-score arrays.
"""


#las funciones que tengo que usar son boundary_scores y aggregated_jaccard_index



"""
Pruebas para la importación de las máscaras usando la api de coco como me dijo Raquel
"""

import os
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













annFile = 'IL6_1_prueba.json'  #IL6_1_prueba.json

coco=COCO(annFile) # funciona

category_ids = coco.getCatIds()
num_categories = len(category_ids)
print('number of categories: ',num_categories)
for ids in category_ids:
    cats = coco.loadCats(ids=ids)
    print(cats)


# Load images for the given ids
image_ids = coco.getImgIds()
image_id = image_ids[0]  # Change this line to display a different image
image_info = coco.loadImgs(image_id)
print(image_info)


# Load annotations for the given ids
annotation_ids = coco.getAnnIds(imgIds=image_id)
annotations = coco.loadAnns(annotation_ids)
print(annotations)

# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create an empty binary mask with the same dimensions as the image
binary_mask2 = np.zeros((height, width), dtype=np.uint8)

import cv2

# Iterate through the annotations and draw the binary masks
for annotation in annotations:
    segmentation = annotation['segmentation']
    mask = coco.annToMask(annotation)                #Esta es la función que me dijo Raquel de usar, la función annToMask

    # Add the mask to the binary mask
    binary_mask2 += mask


# Display the binary mask
plt.figure(figsize=(10,10))
plt.imshow(binary_mask2, cmap='gray')
plt.axis('off')
plt.title('Binary Mask')
#plt.savefig('binary_mask_Image_1029.png', dpi=300)
#plt.show()


print("\n")
print("\n")

print("\n")
#print("Se llama a PIL.features.pilinfo()")

import PIL
#PIL.features.pilinfo()

from PIL import Image

print("\n")
print("\n")


def resize_image(image_array, max_size=512):
    # Convertir el array a una imagen PIL
    img = Image.fromarray(image_array)
    if img.mode not in ('L', 'RGB'):
        img = img.convert('L')
    img.thumbnail((max_size, max_size), Image.NEAREST) #Image.ANTIALIAS   #Image.LANCZOS    #Image.BICUBIC 
    #Flags que generan imágenes de menor calidad: Image.BILINEAR Image.NEAREST
    # Convertir la imagen PIL redimensionada de vuelta a un array
    resized_image_array = np.array(img)
    return resized_image_array

#resized_mask_array = resize_image(mask_array)


dir_mascara_pred = '../Imagenes_para_entrenamiento/IL6_1/Image_1029diamerter300.npy' #Image_1029diamerter300

import numpy as np

masks_pred = np.load(dir_mascara_pred)

print("El tipo de masks_pred es = ")
print(type(masks_pred))

resized_masks_true = resize_image(binary_mask2, 256) # Con 128 funciona pero los valores son una puta mierda

resized_mask_pred = resize_image(masks_pred, 256) # Con 200 funciona pero me llega la RAM al límite

from cellpose.metrics import aggregated_jaccard_index
resultado = aggregated_jaccard_index(resized_masks_true, resized_mask_pred)
#resultado = aggregated_jaccard_index(binary_mask_single_channel, masks_pred)   #binary_mask2
#resultado = aggregated_jaccard_index(binary_mask2, masks_pred)      #Este en principio parece que da algo, en principio debería ser binary_mask pero como estoy haciendo pruebas pues ahora es con el 2
#Según he mirado parece que lo que da lo da bien pues debe dar 0 para el valor del fondo y algo cercano a 1 donde se superpongan ambas máscaras

#resultado = aggregated_jaccard_index(masks_true2, masks_pred)

#print(f"Resultado de aggregated_jaccard_index = :{resultado:.4f}")

print("Resultado de aggregated_jaccard_index = ")
print(resultado)
print("Tipo de \"resultado\" de aggregated_jaccard_index = ")
print(type(resultado))

#valores_positivos = np.where(resultado > 0)    #Sospecho que esto no vale para nada
#print("Resultado de aggregated_jaccard_index (valores positivos) = ")
#print(valores_positivos)

prueba_lista = []

#prueba_lista.append(num_categories)    #num_categories viene de más arriba del código copiado

prueba_lista.append(2)

prueba_list_mask_true = []
#prueba_list_mask_true.append(binary_mask2)
prueba_list_mask_true.append(resized_masks_true)

prueba_list_mask_pred = []
#prueba_list_mask_pred.append(masks_pred)
prueba_list_mask_pred.append(resized_mask_pred)

"""
from skimage.transform import resize

# Reduce el tamaño de las máscaras a una resolución más manejable
target_height = height // 2 #Si lo hago un pelín más pequeño directamente no vale
target_width = width // 2 #Si no da un error por el tema de la memoria lo da por culpa de que al ser muy pequeña desaparecen las segmentaciones

resized_masks_true = [resize(mask, (target_height, target_width), preserve_range=True) for mask in prueba_list_mask_true]
resized_masks_pred = [resize(mask, (target_height, target_width), preserve_range=True) for mask in prueba_list_mask_pred]
"""

from cellpose.metrics import boundary_scores

batch_size = 1000  # Ajusta el tamaño del lote según tu memoria disponible

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

#precision, recall, fscore = process_in_batches(prueba_list_mask_true, prueba_list_mask_pred, batch_size)

precision, recall, fscore = boundary_scores(prueba_list_mask_true, prueba_list_mask_pred, prueba_lista)
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



print("\n")
print("\n")
print("Código que he copiado del kaggle")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print("\n")
print("\n")
























# Load categories for the given ids
ids = 1
cats = coco.loadCats(ids=ids)
print(cats)


#Print categories    ->     Para mirar si está bien
category_ids = coco.getCatIds()
num_categories = len(category_ids)
print('number of categories: ',num_categories)
for ids in category_ids:
    cats = coco.loadCats(ids=ids)
    print(cats)


# Load images for the given ids
image_ids = coco.getImgIds()
image_id = image_ids[0]  # Change this line to display a different image
image_info = coco.loadImgs(image_id)
print(image_info)


# Load annotations for the given ids
annotation_ids = coco.getAnnIds(imgIds=image_id)
annotations = coco.loadAnns(annotation_ids)
print(annotations)


# Get category ids that satisfy the given filter conditions
filterClasses = ['laptop', 'tv', 'cell phone']
# Fetch class IDs only corresponding to the filterClasses
catIds = coco.getCatIds(catNms=filterClasses)
print(catIds)


"""
After executing this code, you will see the category information and the image ID printed in the console or output area. 
The category information includes details about the category with the provided ID, and the image ID corresponds to an image 
that belongs to that category in the COCO dataset.
"""
# Load category information for the given ID
catID = 15
print(coco.loadCats(ids=catID))

# Get image ID that satisfies the given filter conditions
imgId = coco.getImgIds(catIds=[catID])[0]
print(imgId)


#Retrieving Annotation IDs for an Image
ann_ids = coco.getAnnIds(imgIds=[imgId], iscrowd=None)
print(ann_ids)

#Displaying Image with Annotations
print(f"Annotations for Image ID {imgId}:")
anns = coco.loadAnns(ann_ids)

image_path = coco.loadImgs(imgId)[0]['file_name']
print(image_path)
image = plt.imread(imageDir + image_path) #Para que funcione tengo que descomentar una línea de más arriba que usé para hacer pruebas
plt.imshow(image)

# Display the specified annotations
coco.showAnns(anns, draw_bbox=True)

plt.axis('off')
plt.title('Annotations for Image ID: {}'.format(image_id))
plt.tight_layout()
plt.show()


#Displaying Images with Annotations     ->    Creo que es una compilacións del código completo para poder generar una imagen con máscaras.
def main():

    # Category IDs.
    cat_ids = coco.getCatIds()
    print(f"Number of Unique Categories: {len(cat_ids)}")
    print("Category IDs:")
    print(cat_ids)  # The IDs are not necessarily consecutive.

    # All categories.
    cats = coco.loadCats(cat_ids)
    cat_names = [cat["name"] for cat in cats]
    print("Categories Names:")
    print(cat_names)

    # Category ID -> Category Name.
    query_id = cat_ids[0]
    query_annotation = coco.loadCats([query_id])[0]
    query_name = query_annotation["name"]
    query_supercategory = query_annotation["supercategory"]
    print("Category ID -> Category Name:")
    print(
        f"Category ID: {query_id}, Category Name: {query_name}, Supercategory: {query_supercategory}"
    )

    # Category Name -> Category ID.
    query_name = cat_names[2]
    query_id = coco.getCatIds(catNms=[query_name])[0]
    print("Category Name -> ID:")
    print(f"Category Name: {query_name}, Category ID: {query_id}")

    # Get the ID of all the images containing the object of the category.
    img_ids = coco.getImgIds(catIds=[query_id])
    print(f"Number of Images Containing {query_name}: {len(img_ids)}")

    # Pick one image.
    img_id = img_ids[2]
    img_info = coco.loadImgs([img_id])[0]
    img_file_name = img_info["file_name"]
    img_url = img_info["coco_url"]
    print(
        f"Image ID: {img_id}, File Name: {img_file_name}, Image URL: {img_url}"
    )

    # Get all the annotations for the specified image.
    ann_ids = coco.getAnnIds(imgIds=[img_id], iscrowd=None)
    anns = coco.loadAnns(ann_ids)
    print(f"Annotations for Image ID {img_id}:")
    print(anns)

    # Use URL to load image.
    # im = Image.open(requests.get(img_url, stream=True).raw)
    # Load image from dataset
    im = plt.imread(imageDir+ coco.loadImgs(img_id)[0]['file_name'])
    # Save image and its labeled version.
    plt.axis("off")
    plt.imshow(np.asarray(im))
    plt.savefig(f"{img_id}.jpg", bbox_inches="tight", pad_inches=0)
    # Plot segmentation and bounding box.
    coco.showAnns(anns, draw_bbox=True)
    plt.savefig(f"{img_id}_annotated.jpg", bbox_inches="tight", pad_inches=0)
    plt.show()
    return


if __name__ == "__main__":

    main()



#Displaying Filtered Images with Annotations    ->   Creo que no lo necesito para nada, revisar con calma

# Define the classes (out of the 80) which you want to see. Others will not be shown.
filterClasses = ['laptop', 'tv', 'cell phone']

# Fetch class IDs only corresponding to the filterClasses
catIds = coco.getCatIds(catNms=filterClasses)

# Get all images containing the above Category IDs
imgIds = coco.getImgIds(catIds=catIds)

# Load a random image from the filtered list
if len(imgIds) > 0:
    image_id = imgIds[np.random.randint(len(imgIds))]  # Select a random image ID
    image_info = coco.loadImgs(image_id)

    if image_info is not None and len(image_info) > 0:
        image_info = image_info[0]
        image_path = imageDir + image_info['file_name']

        # Load the annotations for the image
        annotation_ids = coco.getAnnIds(imgIds=image_id)
        annotations = coco.loadAnns(annotation_ids)

        # Get category names and assign colors for annotations
        category_names = [coco.loadCats(ann['category_id'])[0]['name'].capitalize() for ann in annotations]
        category_colors = list(matplotlib.colors.TABLEAU_COLORS.values())

        # Load the image and plot it
        image = plt.imread(image_path)
        plt.imshow(image)
        plt.axis('off')
        plt.title('Annotations for Image ID: {}'.format(image_id))
        plt.tight_layout()
        plt.savefig('Img.png',dpi=350)
        plt.show()
        
        plt.imshow(image)
        plt.axis('off')

        # Display bounding boxes and segmented colors for each annotation
        for ann, color in zip(annotations, category_colors):
            bbox = ann['bbox']
            segmentation = ann['segmentation']

            # Display bounding box
            rect = patches.Rectangle((bbox[0], bbox[1]), bbox[2], bbox[3], linewidth=1,
                                     edgecolor=color, facecolor='none')
            plt.gca().add_patch(rect)

            # Display segmentation masks with assigned colors
            for seg in segmentation:
                poly = np.array(seg).reshape((len(seg) // 2, 2))
                plt.fill(poly[:, 0], poly[:, 1], color=color, alpha=0.6)

        # Create a legend with category names and colors
        legend_patches = [patches.Patch(color=color, label=name) for color, name in zip(category_colors, category_names)]
        plt.legend(handles=legend_patches, loc="lower center", ncol=4, bbox_to_anchor=(0.5, -0.2), fontsize='small')

        # Show the image with legend
        plt.title('Annotations for Image ID: {}'.format(image_id))
        plt.tight_layout()
        plt.savefig('annImg.png',dpi=350)
        plt.show()
    else:
        print("No image information found for the selected image ID.")
else:
    print("No images found for the desired classes.")




##Generating Masks for Object Segmentation      -> Creo que es de aquí de donde tengo que sacar las cosas

# Extracting Mask Information
# Load annotations for a specific image ID
# Load images for the given ids
image_ids = coco.getImgIds()
image_id = image_ids[0] 
annotations = coco.loadAnns(coco.getAnnIds(imgIds=image_id))

# Retrieve image file path
image_info = coco.loadImgs(image_id)[0]
image_dir = os.path.join(dataDir, 'images', 'val2014')
image_path = os.path.join(image_dir, image_info['file_name'])

# Load the main image
main_image = plt.imread(image_path)

# Create a new figure for displaying the main image
plt.figure(figsize=(10, 10))
plt.imshow(main_image)
plt.axis('off')
plt.title('Main Image')

# Save the figures
plt.savefig('main_image.png', dpi=300)

# Show the plots
plt.show()

##Generating Binary Masks    ->  Creo que es justo de aquí de donde puedo sacar las máscaras
# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create an empty binary mask with the same dimensions as the image
binary_mask = np.zeros((height, width), dtype=np.uint8)

# Iterate through the annotations and draw the binary masks
for annotation in annotations:
    segmentation = annotation['segmentation']
    mask = coco.annToMask(annotation)                #Esta es la función que me dijo Raquel de usar, la función annToMask

    # Add the mask to the binary mask
    binary_mask += mask

# Display the binary mask
plt.figure(figsize=(10,10))
plt.imshow(binary_mask, cmap='gray')
plt.axis('off')
plt.title('Binary Mask')
plt.savefig('binary_mask.png', dpi=300)
plt.show()

##Generating RGB Mask
# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create an empty RGB mask with the same dimensions as the image
rgb_mask = np.zeros((height, width, 3), dtype=np.uint8)

# Define a color map for different object classes
color_map = {cat['id']: (np.random.randint(0, 256), np.random.randint(0, 256), np.random.randint(0, 256))
             for cat in coco.loadCats(catIDs)}

# Iterate through the annotations and assign unique colors to each class/object
for annotation in annotations:
    category_id = annotation['category_id']
    color = color_map[category_id]

    # Draw the mask on the RGB mask
    mask = coco.annToMask(annotation)
    rgb_mask[mask == 1] = color

# Display the RGB mask
plt.figure(figsize=(10,10))
plt.imshow(rgb_mask)
plt.axis('off')
plt.title('RGB Mask')
plt.savefig('rgb_mask.png', dpi=300)
plt.show()

##Generating Instance Segmentation Mask
# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create an empty mask with the same dimensions as the image
instance_mask = np.zeros((height, width), dtype=np.uint8)

# Iterate through the annotations and draw the instance segmentation masks
for annotation in annotations:
    segmentation = annotation['segmentation']
    mask = coco.annToMask(annotation)
    category_id = annotation['category_id']

    # Assign a unique value to each instance mask
    instance_mask[mask == 1] = category_id

# Display the instance segmentation mask
plt.figure(figsize=(10,10))
plt.imshow(instance_mask, cmap='viridis')
plt.axis('off')
plt.title('Instance Segmentation Mask')
plt.savefig('instance_mask.png', dpi=300)
plt.show()

##Generating Object Detection Bounding Boxes
# Retrieve image dimensions
image_info = coco.loadImgs(image_id)[0]
height, width = image_info['height'], image_info['width']

# Create a new figure with the same dimensions as the image
fig, ax = plt.subplots(figsize=(10,10), dpi=100)

# Display the original image
ax.imshow(main_image)
ax.axis('off')
ax.set_title('Original Image')

# Draw bounding boxes on the original image
for annotation in annotations:
    bbox = annotation['bbox']
    category_id = annotation['category_id']
    category_name = coco.loadCats(category_id)[0]['name']

    # Convert COCO bounding box format (x, y, width, height) to matplotlib format (xmin, ymin, xmax, ymax)
    xmin, ymin, width, height = bbox
    xmax = xmin + width
    ymax = ymin + height

    # Draw the bounding box rectangle
    rect = patches.Rectangle((xmin, ymin), width, height, linewidth=1, edgecolor='red', facecolor='none')
    ax.add_patch(rect)

    # Add the category name as a label above the bounding box
    ax.text(xmin, ymin - 5, category_name, fontsize=8, color='red', weight='bold')

# Save the figure with adjusted dimensions
plt.savefig('bounding_boxes.png', bbox_inches='tight')

# Show the plot
plt.show()


##Post-Processing Techniques
import numpy as np
from scipy.ndimage import binary_erosion, binary_dilation
from scipy.ndimage.filters import gaussian_filter

# Apply erosion to the binary mask
eroded_mask = binary_erosion(binary_mask)

# Apply dilation to the binary mask
dilated_mask = binary_dilation(binary_mask)

# Apply Gaussian blur to the binary mask
smoothed_mask = gaussian_filter(binary_mask, sigma=.2)

# Display the post-processed masks
fig, axes = plt.subplots(3, 1, figsize=(12, 12))

axes[0].imshow(eroded_mask, cmap='gray')
axes[0].set_title('Eroded Mask')
axes[0].axis('off')

axes[1].imshow(dilated_mask, cmap='gray')
axes[1].set_title('Dilated Mask')
axes[1].axis('off')

axes[2].imshow(smoothed_mask, cmap='gray')
axes[2].set_title('Smoothed Mask')
axes[2].axis('off')

plt.tight_layout()
plt.savefig('post_processed_masks.png', dpi=300)
plt.show()


###Evaluation of Generated Masks     ---->    Lugar donde puedo mirar el tema de las métricas
##Intersection over Union (IoU)
import numpy as np

# Ground truth mask
gt_mask = binary_mask.astype(bool)  # Example ground truth mask

# Predicted mask
predicted_mask = smoothed_mask.astype(bool)  # Example predicted mask

# Calculate Intersection over Union (IoU)
intersection = np.logical_and(gt_mask, predicted_mask)
union = np.logical_or(gt_mask, predicted_mask)
iou = np.sum(intersection) / np.sum(union)

# Print the IoU score
print(f"Intersection over Union (IoU): {iou:.4f}")

#El resultado de tío: Intersection over Union (IoU): 0.9161     ---> Lo pongo para saber que es sobre 1










