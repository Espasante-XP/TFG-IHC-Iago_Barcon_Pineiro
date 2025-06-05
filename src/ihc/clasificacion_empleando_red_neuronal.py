
import os, gc
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import cv2
from torchvision import transforms
from pycocotools.coco import COCO
from utils import obter_lista_ficheiros, natural_sort_key, get_final_folder_name
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score, confusion_matrix
import torchvision.models as models
from torch.optim import lr_scheduler



"""
    transforms.RandomResizedCrop(224, scale=(0.8, 1.0)),  # Recorte aleatorio y redimensionado
    transforms.RandomApply([transforms.ColorJitter(brightness=0.2, contrast=0.2)], p=0.5),  # Aumento de brillo y contraste
    transforms.RandomApply([transforms.RandomAffine(degrees=15, translate=(0.1, 0.1), scale=(0.9, 1.1))], p=0.5),  # Aumento de rotación y traslación
    transforms.RandomApply([transforms.GaussianBlur(kernel_size=3)], p=0.5),  # Aumento de desenfoque gaussiano
    transforms.RandomApply([transforms.RandomGrayscale(p=0.1)], p=0.5),  # Aumento de escala de grises
    transforms.RandomApply([transforms.RandomErasing(p=0.5)], p=0.5),  # Aumento de borrado aleatorio
    transforms.RandomApply([transforms.RandomPerspective(distortion_scale=0.5, p=0.5)], p=0.5),  # Aumento de perspectiva
"""

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


dir_general_directorios_train = "../../Imagenes_entrenamiento/"

dir_general_anotaciones = "./anotaciones_coco_v2/"

# Obtener las regiones y etiquetas de las imágenes
lista_total_cell_regions, lista_total_labels = obtener_regiones_y_etiquetas(dir_general_directorios_train, dir_general_anotaciones)


X_train = np.array(lista_total_cell_regions)
y_train = np.array(lista_total_labels)

print("Valores mínimos y máximos de las etiquetas:", np.min(y_train), np.max(y_train))
print("Número total de etiquetas:", len(y_train))
#print("Ejemplo de etiquetas:", y_train[:10])


lista_total_cell_regions = []
lista_total_labels = []

dir_general_directorios_test = "../../Imagenes_validacion/"

lista_total_cell_regions, lista_total_labels = obtener_regiones_y_etiquetas(dir_general_directorios_test, dir_general_anotaciones)

X_val = np.array(lista_total_cell_regions)
y_val = np.array(lista_total_labels)


# Cargar ResNet18 preentrenado en ImageNet
model = models.resnet18(weights='IMAGENET1K_V1')  # Modelo preentrenado

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print("Usando dispositivo:", device)

# Ajustar la última capa para tu número de clases (4 en este caso)
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # Reemplazar la capa final
model = model.to(device)  # Mover al dispositivo (CPU/GPU)


learning_rate = 0.001  
momentum = 0.9  # Momento para el optimizador
step_size = 7  # Número de épocas antes de reducir el learning rate
gamma = 0.1  # Factor de reducción del learning rate

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


train_dataset = CellDataset(X_train, y_train, transform=transform)
train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)

val_dataset = CellDataset(X_val, y_val, transform=transform) 
val_loader = DataLoader(val_dataset, batch_size=8, shuffle=False)


numero_epochs = 100  # Número de épocas para el entrenamiento
patience = 10

# A lo mejor sería bueno poner 0.5 o un poco menos, para eso están las pruebas
valor_perdidas_aceptable = 0.1  # Valor de pérdidas aceptable para detener el entrenamiento anticipadamente
best_loss = float('inf') 
counter = 0  # Contador para early stopping

path_modelo = "../../models/clasificador_reentrenado.pth"

gc.collect()  
""""""
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
    
    scheduler.step()  # Actualizar el scheduler

    gc.collect()  # Limpiar la memoria de la GPU

    # Lógica de early stopping y guardado del modelo (sin cambios)
    print(f"Epoch {epoch+1}, Train Loss: {loss.item():.4f}, Val Loss: {val_loss:.4f}")
    # Early stopping
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), "../../models/clasificador_reentrenado.pth")
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping, no improvement in validation loss for", patience, "epochs.")
            break

    # Parada temprana 2
    if(loss.item() < valor_perdidas_aceptable):
        print(f"Entrenamiento detenido anticipadamente en la época {epoch+1} con pérdida {loss.item()}")
        break




""" Código modificado por mi para entrenar el modelo
numero_epochs = 10000  # Número de épocas para el entrenamiento

best_loss = float('inf') 

valor_perdidas_aceptable = 0.1  # Valor de pérdidas aceptable para detener el entrenamiento anticipadamente

# Estes valores no son representativos de verdad, de momento, porque estoy probando todo con una sola imagen y 11 células
patience = 100 # 10
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

    # Early stopping
    if val_loss < best_loss:
        best_loss = val_loss
        counter = 0
        torch.save(model.state_dict(), "best_model.pth")
    else:
        counter += 1
        if counter >= patience:
            print("Early stopping")
            break

    # Parada temprana 2
    if(loss.item() < valor_perdidas_aceptable):
        print(f"Entrenamiento detenido anticipadamente en la época {epoch+1} con pérdida {loss.item()}")
        break    
"""



gc.collect()  

# Cargar el modelo guardado para poder realizar la clasificación de tinciones
model = models.resnet18(weights=None)  # Sin preentrenamiento
num_ftrs = model.fc.in_features
model.fc = nn.Linear(num_ftrs, 4)  # Capa final para 4 clases

# Cargar los pesos guardados
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load(path_modelo, map_location=device))
model.to(device)
model.eval() # Modo evaluación


dir_general_directorios_test = "../../Imagenes_validacion/"

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


#print("Índices de clasificación de tinciones:", indices_clasificacion)
#print("Valores de tinción esperados:", y_val)

y_val = lista_total_labels

precision = precision_score(y_val, indices_clasificacion, average='weighted')
recall = recall_score(y_val, indices_clasificacion, average='weighted')
f1 = f1_score(y_val, indices_clasificacion, average='weighted')
accuracy = accuracy_score(y_val, indices_clasificacion)
matriz_confusion = confusion_matrix(y_val, indices_clasificacion, labels=[0, 1, 2, 3])

print(f"Precisión: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"Accuracy: {accuracy:.4f}")

# Imprimir la matriz de confusión
print("Matriz de confusión:")
print(matriz_confusion)

gc.collect()  

exit(0)
