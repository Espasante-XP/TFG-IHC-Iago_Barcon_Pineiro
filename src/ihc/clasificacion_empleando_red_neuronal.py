
import os, gc
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import cv2
from torchvision import transforms
from pycocotools.coco import COCO
from utils import obter_lista_ficheiros, natural_sort_key, get_final_folder_name

from albumentations import Compose, RandomRotate90, Flip

from albumentations.pytorch import ToTensorV2
from albumentations import RandomBrightnessContrast, HueSaturationValue, Normalize


# Todos los transforms me los ha generado la IA, tengo que revisar que sean correctos y que se apliquen bien

transform3 = Compose([
    RandomBrightnessContrast(p=0.5),
    HueSaturationValue(p=0.5),
    Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2()
])



transform2 = Compose([RandomRotate90(), Flip(p=0.5)])



# De momento lo meto aquí arriba para más comodidad pero luego lo tengo que poner donde toca
# Transformaciones para la normalización y aumento de datos
transform = transforms.Compose([
    transforms.ToPILImage(),  # Convertir numpy.ndarray a PIL.Image
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomVerticalFlip(p=0.5),
    transforms.RandomRotation(30),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor(),  # Volver a convertir a tensor
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalización estándar
])

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
        cell_region = cv2.resize(cell_region, (64, 64))  # Usando OpenCV
        cell_regions.append(cell_region)
    return np.array(cell_regions)

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

# Arquitectura en PyTorch
class CNNClassifier(nn.Module): # Tiene que se una red neuronal de clasificación de tipo softmax según he mirado
    """
    Definición de una red neuronal convolucional simple para clasificar las tinciones de células.
    """
    def __init__(self):
        super().__init__()
        self.model = nn.Sequential( # Tengo que revisar todo esto que la verdad no estoy del todo seguro de si son suficientes capas y si
                                        # los tamaños están bien
            nn.Conv2d(3, 32, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Flatten(),
            nn.Linear(64*14*14, 64),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(64, 4),
        )

    def forward(self, x):
        return self.model(x)

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


""" Mi código para cargar una imagen y su máscara
ruta_imagen = '../../Imagenes_entrenamiento/Control_negativo_1/Image_994.jpg'
ruta_mascara = '../../Imagenes_entrenamiento/Control_negativo_1/Image_994_ground_truth.npy'

# Seica es interesante normalizar los valores de la imagen a [0, 1] o [0, 255] dependiendo de la red neuronal que se use para ayudar a la convergencia
image = cv2.imread(ruta_imagen, cv2.COLOR_BGR2RGB) # Fuerzo a que la imagen se cargue en formato RGB porque OpenCV la carga en BGR por defecto
mask = np.load(ruta_mascara) 

# Tengo que hacer un bucle para cargar todas las imágenes de la carpeta de Control_negativo_1, para las anotaciones a lo mejor miro
# de obtenerlas directamente de las anotaciones COCO de paso que obtengo las tinciones de las células

cell_regions = extract_cell_regions(image, mask)

array_valores_tincion = [2, 2, 2, 0, 1, 2, 1, 1, 1, 2, 0] # Los valores de tinción de cada una de las células de Image_994 de Control_negativo_1

labels = np.array(array_valores_tincion) 
print("Tensor de etiquetas:", torch.tensor(labels))
print("Tipo de tensor:", torch.tensor(labels).dtype)
"""


# Carpetas he escogido aleatoriamente para las pruebas para entrenar el modelo: Control_negativo_2, IL6_2, MS BC RMB_1 y MS FNB RMB_1
dir_imagenes = ["../../Imagenes_entrenamiento/Control_negativo_2", "../../Imagenes_entrenamiento/IL6_2", "../../Imagenes_entrenamiento/MS BC RMB_1", "../../Imagenes_entrenamiento/MS FNB RMB_1"]

dir_general_anotaciones = "./anotaciones_coco_v2/"

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

        image_info = coco.loadImgs(image_id)
        if not image_info:
            print(f"Error al cargar información de la imagen con ID {image_id}")
            continue
        image_info = image_info[0]
        nombre_imagen = image_info['file_name']
        #print(f"Nombre de la imagen: {nombre_imagen}")
        #print("Valores mínimos y máximos de las etiquetas:", np.min(valores_tincion), np.max(valores_tincion))

    print(f"Directorio: {directorio}")
    print("Valores mínimos y máximos de las etiquetas:", np.min(lista_aux_labels), np.max(lista_aux_labels))

    if(len(lista_aux_regiones) == 0 or len(lista_aux_labels) == 0):
        print(f"Advertencia: No se encontraron regiones de células o etiquetas en el directorio {directorio}.")
        continue

    if(len(lista_aux_regiones) != len(lista_aux_labels)):
        print(f"Advertencia: El número de regiones de células ({len(lista_aux_regiones)}) no coincide con el número de etiquetas ({len(lista_aux_labels)}) en el directorio {directorio}.")
        continue

    lista_total_cell_regions.extend(lista_aux_regiones) # Añadir las regiones de células a la lista total
    lista_total_labels.extend(lista_aux_labels)


gc.collect()  

all_cell_regions = np.array(lista_total_cell_regions)
all_labels = np.array(lista_total_labels)

print("Valores mínimos y máximos de las etiquetas:", np.min(all_labels), np.max(all_labels))
print("Número total de etiquetas:", len(all_labels))
print("Ejemplo de etiquetas:", all_labels[:10])


X_train, X_val, y_train, y_val = train_test_split(
    all_cell_regions, all_labels, test_size=0.2, random_state=42
)


# DataLoader
train_dataset = CellDataset(X_train, y_train, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

# A lo mejor debería poner todo esto más abajo, justo antes del entrenamiento
val_dataset = CellDataset(X_val, y_val, transform=None)  # Sin aumentos en validación todavía
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)




model = CNNClassifier()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Usando dispositivo:", device)

model.to(device)

criterion = nn.CrossEntropyLoss()
learning_rate = 0.005 # 0.001 
optimizer = optim.Adam(model.parameters(), lr=learning_rate)


numero_epochs = 10000  # Número de épocas para el entrenamiento

best_loss = float('inf') # Valor que se tiene que mejorar

valor_perdidas_aceptable = 0.1  # Valor de pérdidas aceptable para detener el entrenamiento anticipadamente

# Estes valores no son representativos de verdad, de momento, porque estoy probando todo con una sola imagen y 11 células
patience = 300 # 10 
counter = 0

for epoch in range(numero_epochs):
    # Entrenamiento
    model.train()
    for images, labels in train_loader:
        images, labels = images.to(device), labels.to(device)
        outputs = model(images)
        loss = criterion(outputs, labels)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # Validación
    model.eval()
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

    val_loss /= len(val_loader)
    accuracy = 100 * correct / total
    print(f"Epoch {epoch+1}, Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}, Accuracy: {accuracy:.2f}%")

    # Parada temprana
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), "best_model.pth")
    else:
        counter += 1
        if counter >= patience:
            print("Parada temprana")
            break

    # Parada temprana 2
    if(loss.item() < valor_perdidas_aceptable):
        print(f"Entrenamiento detenido anticipadamente en la época {epoch+1} con pérdida {loss.item()}")
        break    






ruta_imagen = '../../Imagenes_entrenamiento/Control_negativo_1/Image_994.jpg'
ruta_mascara = '../../Imagenes_entrenamiento/Control_negativo_1/Image_994_ground_truth.npy'

# Seica es interesante normalizar los valores de la imagen a [0, 1] o [0, 255] dependiendo de la red neuronal que se use para ayudar a la convergencia
image = cv2.imread(ruta_imagen, cv2.COLOR_BGR2RGB) # Fuerzo a que la imagen se cargue en formato RGB porque OpenCV la carga en BGR por defecto
mask = np.load(ruta_mascara) 

array_valores_tincion = [2, 2, 2, 0, 1, 2, 1, 1, 1, 2, 0] # Los valores de tinción de cada una de las células de Image_994 de Control_negativo_1

# Creo que lo de poner aquí directamente lo de image y mask no es lo correcto, pero como es un ejemplo de prueba lo dejo así
indices_clasificacion = classify_staining(model, image, mask)
print("Índices de clasificación de tinciones:", indices_clasificacion)
print("Valores de tinción esperados:", array_valores_tincion)

