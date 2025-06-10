
import os, gc
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2
from torchvision import transforms
from pycocotools.coco import COCO
from utils import obter_lista_ficheiros, natural_sort_key, get_final_folder_name, es_num_positivo_string, es_ruta_valida
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
import torchvision.models as models
from torch.optim import lr_scheduler
import json
from pathlib import Path


path_folder_metrics = '../../resultados/clasificacion_tincion/'


# Función para extraer regiones de células
def extract_cell_regions(image: np.ndarray, mask: np.ndarray):
    """
    Extrae regiones de células de una imagen basándose en una máscara de segmentación.
     :param image (np.ndarray): Imagen original en formato RGB.
     :param mask (np.ndarray): Máscara de segmentación donde cada píxel representa una etiqueta de célula.
                             Las etiquetas deben ser enteros consecutivos empezando en 1.
     :return: cell_regions (np.ndarray): Array de regiones de células extraídas, cada una redimensionada a 64x64 píxeles.
    """
    cell_regions = []
    unique_labels = np.unique(mask)[1:]
    for label in unique_labels:
        coords = np.where(mask == label)
        min_row, max_row = np.min(coords[0]), np.max(coords[0])
        min_col, max_col = np.min(coords[1]), np.max(coords[1])
        cell_region = image[min_row:max_row+1, min_col:max_col+1]
        cell_region = cv2.resize(cell_region, (224, 224))  # Redimensionar a 224x224 píxeles para ResNet18
        cell_regions.append(cell_region)
    return np.array(cell_regions)

 
def obtener_regiones_y_etiquetas(directorio_general, dir_general_anotaciones):
    """
    Obtiene las regiones de células y sus etiquetas de tinción a partir de un directorio general que contiene subdirectorios con imágenes y máscaras.
        :param directorio_general (str): Ruta al directorio general que contiene subdirectorios con imágenes y máscaras.
        :param dir_general_anotaciones (str): Ruta al directorio general que contiene las anotaciones COCO.
        :return: lista_total_cell_regions (list): Lista de regiones de células extraídas.
        :return: lista_total_labels (list): Lista de etiquetas de tinción correspondientes a las regiones de células.
    """

    dir_imagenes = [name for name in os.listdir(directorio_general) if os.path.isdir(os.path.join(directorio_general, name))]

    dir_imagenes = [os.path.join(directorio_general, name) for name in dir_imagenes if os.path.isdir(os.path.join(directorio_general, name))]

    lista_total_cell_regions = []
    lista_total_labels = [] # Los labels son las tinciones de las células

    for directorio in dir_imagenes:
        lista_aux_regiones = []
        lista_aux_labels = []

        lista_imagenes = obter_lista_ficheiros(directorio, ".jpg")
        lista_mascaras = obter_lista_ficheiros(directorio, ".npy")
        lista_imagenes_ordenada = sorted(lista_imagenes, key=natural_sort_key)
        lista_mascaras_ordenada = sorted(lista_mascaras, key=natural_sort_key)
        for imagen, mascara in zip(lista_imagenes_ordenada, lista_mascaras_ordenada):
            image = cv2.imread(imagen, cv2.COLOR_BGR2RGB) # Fuerzo a que la imagen se cargue en formato RGB porque OpenCV la carga en BGR por defecto
            mask = np.load(mascara)
            cell_regions = extract_cell_regions(image, mask)
            lista_aux_regiones.extend(cell_regions)  # Añadir las regiones de células a la lista auxiliar
            gc.collect()  

        nombre_dir = get_final_folder_name(directorio)
        dir_anotaciones = os.path.join(dir_general_anotaciones, nombre_dir)
        fichero_anotaciones = obter_lista_ficheiros(dir_anotaciones, ".json")

        coco = COCO(fichero_anotaciones[0])  # Asumiendo que hay un único fichero de anotaciones por directorio (siempre debería ser así)
        image_ids = coco.getImgIds()
        for image_id in image_ids:
            ann_ids = None
            annotations = None
            valores_tincion = []
            ann_ids = coco.getAnnIds(imgIds=image_id)
            annotations = coco.loadAnns(ann_ids)
            valores_tincion = [ann['category_id'] for ann in annotations if 'category_id' in ann]

            if np.max(valores_tincion) == 4 and np.min(valores_tincion) > 0: # Hay anotaciones que están en rango [1, 4],
                                                                                # pero otras que están en rango [0, 3]
                valores_tincion = [v - 1 for v in valores_tincion]

            lista_aux_labels.extend(valores_tincion)  # Añadir las etiquetas a la lista auxiliar
            gc.collect()  

        if(len(lista_aux_regiones) == 0 or len(lista_aux_labels) == 0):
            print(f"Advertencia: No se encontraron regiones de células o etiquetas en el directorio {directorio}.")
            print("Se omite este directorio.")
            continue

        if(len(lista_aux_regiones) != len(lista_aux_labels)):
            print(f"Advertencia: El número de regiones de células ({len(lista_aux_regiones)}) no coincide con el número de etiquetas ({len(lista_aux_labels)}) en el directorio {directorio}.")
            print("Se omite este directorio.")
            continue

        lista_total_cell_regions.extend(lista_aux_regiones) # Añadir las regiones de células a la lista total
        lista_total_labels.extend(lista_aux_labels)
        gc.collect() 
    gc.collect()  
    return lista_total_cell_regions, lista_total_labels


def obtener_regiones_y_etiquetas_y_guardar_imagenes_celulas(directorio_general, dir_general_anotaciones):
    # Crear las 4 carpetas en el directorio general
    carpeta_guardado = "../../secciones_celulas/"
    base_save_dir = os.path.join(carpeta_guardado, "tincion_grupos")
    for label in range(4):  # Asumimos que las tinciones son 0, 1, 2, 3
        os.makedirs(os.path.join(base_save_dir, f"tincion_{label}"), exist_ok=True)

    dir_imagenes = [name for name in os.listdir(directorio_general) if os.path.isdir(os.path.join(directorio_general, name))]
    dir_imagenes = [os.path.join(directorio_general, name) for name in dir_imagenes if os.path.isdir(os.path.join(directorio_general, name))]

    lista_total_cell_regions = []
    lista_total_labels = []

    for directorio in dir_imagenes:
        lista_aux_regiones = []
        lista_aux_labels = []

        lista_imagenes = obter_lista_ficheiros(directorio, ".jpg")
        lista_mascaras = obter_lista_ficheiros(directorio, ".npy")
        lista_imagenes_ordenada = sorted(lista_imagenes, key=natural_sort_key)
        lista_mascaras_ordenada = sorted(lista_mascaras, key=natural_sort_key)

        for imagen, mascara in zip(lista_imagenes_ordenada, lista_mascaras_ordenada):
            image = cv2.imread(imagen, cv2.COLOR_BGR2RGB)
            mask = np.load(mascara)
            cell_regions = extract_cell_regions(image, mask)
            lista_aux_regiones.extend(cell_regions)

        nombre_dir = get_final_folder_name(directorio)
        dir_anotaciones = os.path.join(dir_general_anotaciones, nombre_dir)
        fichero_anotaciones = obter_lista_ficheiros(dir_anotaciones, ".json")

        coco = COCO(fichero_anotaciones[0])
        image_ids = coco.getImgIds()
        for image_id in image_ids:
            ann_ids = coco.getAnnIds(imgIds=image_id)
            annotations = coco.loadAnns(ann_ids)
            valores_tincion = [ann['category_id'] for ann in annotations if 'category_id' in ann]

            if np.max(valores_tincion) == 4 and np.min(valores_tincion) > 0:
                valores_tincion = [v - 1 for v in valores_tincion]

            lista_aux_labels.extend(valores_tincion)

        if len(lista_aux_regiones) == 0 or len(lista_aux_labels) == 0:
            print(f"Advertencia: No se encontraron regiones de células o etiquetas en el directorio {directorio}.")
            print("Se omite este directorio.")
            continue

        if len(lista_aux_regiones) != len(lista_aux_labels):
            print(f"Advertencia: El número de regiones de células ({len(lista_aux_regiones)}) no coincide con el número de etiquetas ({len(lista_aux_labels)}) en el directorio {directorio}.")
            print("Se omite este directorio.")
            continue

        # Guardar las regiones de células en las carpetas correspondientes
        for idx, (region, label) in enumerate(zip(lista_aux_regiones, lista_aux_labels)):
            # Convertir la región a formato adecuado para guardar
            region_uint8 = (region * 255).astype(np.uint8) if region.max() <= 1.0 else region.astype(np.uint8)
            # Convertir de RGB a BGR para guardar correctamente con cv2.imwrite
            region_bgr = cv2.cvtColor(region_uint8, cv2.COLOR_RGB2BGR)
            filename = f"{nombre_dir}_cell_{idx}.png"
            save_path = os.path.join(base_save_dir, f"tincion_{label}", filename)
            cv2.imwrite(save_path, region_bgr)

        lista_total_cell_regions.extend(lista_aux_regiones)
        lista_total_labels.extend(lista_aux_labels)
        gc.collect()

    return lista_total_cell_regions, lista_total_labels


# Dataset personalizado para PyTorch
class CellDataset(Dataset):
    """
    Dataset personalizado para cargar imágenes de células y sus etiquetas.
     :param images (np.ndarray): Array de imágenes de células.
     :param labels (np.ndarray): Array de etiquetas correspondientes a las imágenes.
     :param transform (callable, optional): Transformación a aplicar a las imágenes.
    """

    def __init__(self, images, labels, transform=None):
        self.images = images
        self.labels = labels
        self.transform = transform

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = self.images[idx]
        label = self.labels[idx]
        if self.transform:
            image = self.transform(image)
        else:
            image = torch.tensor(image, dtype=torch.float32).permute(2, 0, 1)  # [C, H, W]
        return image, torch.tensor(label, dtype=torch.long)


# Clasificación de nuevas células
def classify_staining(model, image, mask): # Según entiendo, esta es la función que debo usar tras entrenar el modelo
    """
    Clasifica las tinciones de las células en una imagen dada una máscara de segmentación.
     :param model (nn.Module): Modelo de red neuronal entrenado para clasificar las tinciones.
     :param image (np.ndarray): Imagen original en formato RGB.
     :param mask (np.ndarray): Máscara de segmentación donde cada píxel representa una etiqueta de célula.
                             Las etiquetas deben ser enteros consecutivos empezando en 1.
     :return: indices_clasificacion (np.ndarray): Array de índices de clasificación de tinciones para cada célula.
    """
    regions = extract_cell_regions(image, mask)
    regions = torch.tensor(regions, dtype=torch.float32).permute(0, 3, 1, 2).to(device)
    with torch.no_grad():
        predictions = model(regions)
    return torch.argmax(predictions, dim=1).cpu().numpy()



archivo_json = '../../config/entrenamiento_clasificacion.json'

archivo_abierto = open(archivo_json)

nombre_path_entrenamiento = "path_entrenamiento"

nombre_path_validacion = "path_validacion"

nombre_path_anotaciones = "path_anotaciones"

nombre_path_guardado_modelo = "path_guardado_modelo"

nombre_learning_rate = "learning_rate"

nombre_momentum = "momentum"

nombre_step_size = "step_size"

nombre_gamma = "gamma"

nombre_numero_epochs = "numero_epochs"

nombre_batch_size = "batch_size"

nombre_patience = "patience"

nombre_valor_perdidas_aceptable = "valor_perdidas_aceptable"

nombre_archivo_resultante = "archivo_resultante"

nombre_data_augmentation = "data_augmentation"

valores_parametros_modelo = json.load(archivo_abierto)

# Comprobaciones de que los valores cargados son correctos
texto_valor_path_entrenamiento = valores_parametros_modelo[nombre_path_entrenamiento]
if(Path(texto_valor_path_entrenamiento).exists() and Path(texto_valor_path_entrenamiento).is_dir()):
    dir_general_directorios_train = texto_valor_path_entrenamiento
else:
    print("Error, el valor introducido para el directorio de entrenamiento no es válido")
    exit()


texto_valor_path_validacion = valores_parametros_modelo[nombre_path_validacion]
if(Path(texto_valor_path_validacion).exists() and Path(texto_valor_path_validacion).is_dir()):
    dir_general_directorios_test = texto_valor_path_validacion
else:
    print("Error, el valor introducido para el directorio de validación no es válido")
    exit()


# Se debe pasar un directorio general de ground truth, que contenga subdirectorios con las anotaciones COCO cuyos nombres coincidan con los de las carpetas de imágenes
texto_valor_path_anotaciones = valores_parametros_modelo[nombre_path_anotaciones]

if(Path(texto_valor_path_anotaciones).exists() and Path(texto_valor_path_anotaciones).is_dir()):
    dir_general_anotaciones = texto_valor_path_anotaciones 
else:
    print("Error, el valor introducido para el directorio de anotaciones no es válido")
    exit()


texto_valor_path_guardado_modelo = valores_parametros_modelo[nombre_path_guardado_modelo]
if es_ruta_valida(texto_valor_path_guardado_modelo):
    if Path(texto_valor_path_guardado_modelo).exists():
        print("Advertencia, el directorio de guardado del modelo ya existe, se sobreescribirá")
    path_guardado_modelo = texto_valor_path_guardado_modelo
else:
    print("Error, el valor introducido para el path de guardado del modelo no es válido")
    exit()


texto_valor_learning_rate = valores_parametros_modelo[nombre_learning_rate]
if es_num_positivo_string(texto_valor_learning_rate) and float(texto_valor_learning_rate) < 1:
    learning_rate = float(texto_valor_learning_rate)
else:
    print("Error, el valor introducido para el learning rate no es válido")
    exit()


texto_valor_momentum = valores_parametros_modelo[nombre_momentum]
if es_num_positivo_string(texto_valor_momentum) and float(texto_valor_momentum) < 1:
    momentum = float(texto_valor_momentum)
else:
    print("Error, el valor introducido para el momentum no es válido")
    exit()


texto_valor_step_size = valores_parametros_modelo[nombre_step_size]
if es_num_positivo_string(texto_valor_step_size):
    step_size = int(texto_valor_step_size)
else:
    print("Error, el valor introducido para el step size no es válido")
    exit()


texto_valor_gamma = valores_parametros_modelo[nombre_gamma]
if es_num_positivo_string(texto_valor_gamma) and float(texto_valor_gamma) < 1:
    gamma = float(texto_valor_gamma)
else:
    print("Error, el valor introducido para el gamma no es válido")
    exit()


texto_numero_epochs = valores_parametros_modelo[nombre_numero_epochs]
if es_num_positivo_string(texto_numero_epochs):
    numero_epochs = int(texto_numero_epochs)
else:
    print("Error, el valor introducido para el número de épocas no es válido")
    exit()


texto_valor_batch_size = valores_parametros_modelo[nombre_batch_size]
if es_num_positivo_string(texto_valor_batch_size):
    batch_size = int(texto_valor_batch_size)
else:
    print("Error, el valor introducido para el batch size no es válido")
    exit()


texto_valor_patience = valores_parametros_modelo[nombre_patience]
if es_num_positivo_string(texto_valor_patience):
    patience = int(texto_valor_patience)
else:
    print("Error, el valor introducido para la paciencia (patience) no es válido")
    exit()


texto_valor_valor_perdidas_aceptable = valores_parametros_modelo[nombre_valor_perdidas_aceptable]
if es_num_positivo_string(texto_valor_valor_perdidas_aceptable):
    valor_perdidas_aceptable = float(texto_valor_valor_perdidas_aceptable)
else:
    print("Error, el valor introducido para el valor de pérdidas aceptable no es válido")
    exit()


texto_valor_archivo_resultante = valores_parametros_modelo[nombre_archivo_resultante]
if isinstance(texto_valor_archivo_resultante, str) and len(texto_valor_archivo_resultante) > 0:
    archivo_resultante = texto_valor_archivo_resultante
else:
    print("Error, el valor introducido para el archivo resultante no es válido")
    exit()


texto_valor_nombre_data_augmentation = valores_parametros_modelo[nombre_data_augmentation]
if (texto_valor_nombre_data_augmentation.isalpha() and texto_valor_nombre_data_augmentation.lower() == "true"):
    data_augmentation = True
elif (texto_valor_nombre_data_augmentation.isalpha() and texto_valor_nombre_data_augmentation.lower() == "false"):
    data_augmentation = False
else:
    print("Error, el valor introducido para realizar o no data augmentation no es válido")
    exit()


# Obtener las regiones y etiquetas de las imágenes
lista_total_cell_regions, lista_total_labels = obtener_regiones_y_etiquetas(dir_general_directorios_train, dir_general_anotaciones)


X_train = np.array(lista_total_cell_regions)
y_train = np.array(lista_total_labels)


gc.collect()  

lista_total_cell_regions = []
lista_total_labels = []

lista_total_cell_regions, lista_total_labels = obtener_regiones_y_etiquetas(dir_general_directorios_test, dir_general_anotaciones)

X_val = np.array(lista_total_cell_regions)
y_val = np.array(lista_total_labels)

gc.collect()

# Cargar ResNet18 preentrenado en ImageNet
model = models.resnet18(weights='IMAGENET1K_V1')  # Modelo preentrenado

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Usando dispositivo:", device)

# Ajustar la última capa para tu número de clases (4 en este caso)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # Reemplazar la capa final
model = model.to(device)  # Mover al dispositivo (CPU/GPU)


# Optimizador para fine-tuning (ajusta todos los parámetros)
optimizer = optim.SGD(model.parameters(), lr=learning_rate, momentum=momentum)

# Scheduler para reducir el learning rate
scheduler = lr_scheduler.StepLR(optimizer, step_size=step_size, gamma=gamma)

criterion = nn.CrossEntropyLoss()


# Transformaciones para la normalización y aumento de datos
transform = transforms.Compose([
    transforms.ToPILImage(),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    transforms.RandomRotation(30),
    transforms.RandomApply([
        transforms.ColorJitter(brightness=0.2, contrast=0.2, saturation=0.2, hue=0.1) # Hue en 0.1 es una variación de +-18º
    ], p=0.5),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]) # Normalización estándar para ResNet18
])


if data_augmentation:
    train_dataset = CellDataset(X_train, y_train, transform=transform)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False) 

    val_dataset = CellDataset(X_val, y_val, transform=transform) 
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
else:
    train_dataset = CellDataset(X_train, y_train, transform=None)
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=False) 

    val_dataset = CellDataset(X_val, y_val, transform=None) 
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)

best_loss = float('inf') 
counter = 0  # Contador para early stopping

gc.collect()  

# Entrenamiento con validación y early stopping
for epoch in range(numero_epochs):
    model.train()  # Modo entrenamiento
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        gc.collect()  
    
    model.eval()  # Modo evaluación
    val_loss = 0.0
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            val_loss += criterion(outputs, labels).item()
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            gc.collect()  
    
    scheduler.step()  # Actualizar el scheduler

    gc.collect()  # Limpiar la memoria de la GPU

    # Lógica de early stopping y guardado del modelo (sin cambios)
    print(f"Epoch {epoch+1}, Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}")

    # Early stopping
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), path_guardado_modelo)
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping, no improvement in validation loss for", patience, "epochs.")
            break

    # Parada temprana 2
    if(loss.item() < valor_perdidas_aceptable):
        print(f"Entrenamiento detenido anticipadamente en la época {epoch+1} con pérdida {loss.item()}")
        break


gc.collect()  




# Cargar el modelo guardado para poder realizar la clasificación de tinciones
model = models.resnet18(weights=None)  # Sin preentrenamiento
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # Capa final para 4 clases

# Cargar los pesos guardados
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load(path_guardado_modelo, map_location=device))
model.to(device)
model.eval() # Modo evaluación


dir_imagenes = [name for name in os.listdir(dir_general_directorios_test) if os.path.isdir(os.path.join(dir_general_directorios_test, name))]

dir_imagenes = [os.path.join(dir_general_directorios_test, name) for name in dir_imagenes if os.path.isdir(os.path.join(dir_general_directorios_test, name))]

for directorio in dir_imagenes:
    imagenes = obter_lista_ficheiros(directorio, ".jpg")
    mascaras = obter_lista_ficheiros(directorio, ".npy")

indices_clasificacion = []

for imagen, mascara in zip(imagenes, mascaras):
    indices_clasificacion_aux = []
    image = cv2.imread(imagen, cv2.COLOR_BGR2RGB) 
    mask = np.load(mascara)
    indices_clasificacion_aux = classify_staining(model, image, mask)
    indices_clasificacion.extend(indices_clasificacion_aux)


lista_total_cell_regions, lista_total_labels = obtener_regiones_y_etiquetas(dir_general_directorios_test, dir_general_anotaciones)

y_val = lista_total_labels

precision = precision_score(lista_total_labels, indices_clasificacion, average='weighted')
recall = recall_score(lista_total_labels, indices_clasificacion, average='weighted')
f1 = f1_score(lista_total_labels, indices_clasificacion, average='weighted')
accuracy = accuracy_score(lista_total_labels, indices_clasificacion)
matriz_confusion = confusion_matrix(lista_total_labels, indices_clasificacion, labels=[0, 1, 2, 3])


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

gc.collect()  

exit(0)
