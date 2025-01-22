import numpy as np
from cellpose import models, train
import os
import cv2


# Cargar el modelo existente con soporte para GPU
model = models.Cellpose(gpu=True, model_type='cyto3')  # Cambiado a gpu=True

def guardar_elementos_de_carpeta(ruta_carpeta, variable_destino, extension):
    for carpeta_raiz, _, archivos in os.walk(ruta_carpeta):
        for nombre_archivo in archivos:
            if nombre_archivo.endswith(extension):
                ruta_imagen = os.path.join(carpeta_raiz, nombre_archivo)
                variable_destino.append(ruta_imagen)

"""
# Ejemplo de uso
ruta_carpeta = './Imagenes_para_entrenamiento'
variable_destino = []
extension = '.jpg'
guardar_elementos_de_carpeta(ruta_carpeta, variable_destino, extension)

# Imprimir los archivos encontrados
for ruta in variable_destino:
    print(ruta)
"""



"""
# Preparar tus datos de entrenamiento
ruta_carpeta_entrenamiento1 = '../Imagenes_para_entrenamiento/Control negativo 3'
ruta_carpeta_entrenamiento2 = '../Imagenes_para_entrenamiento/MS FNB RMB_1'


X_train_paths = []
extension = '.jpg'
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento1, X_train_paths, extension)
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento2, X_train_paths, extension)

extension2 = '.npy'
y_train_aux = []
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento1, y_train_aux, extension2)
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento2, y_train_aux, extension2)

"""


ruta_carpeta_entrenamiento_def = '../Imagenes_entrenamiento/'
path_resultado = []

extension = '.jpg'

X_train_paths = []

guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, path_resultado, extension)
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, X_train_paths, extension)

y_train_aux = []

extension2 = '.npy'

guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, path_resultado, extension2)
guardar_elementos_de_carpeta(ruta_carpeta_entrenamiento_def, y_train_aux, extension2)


#print("path_resultado:", path_resultado)
print("len(path_resultado):", len(path_resultado))
print('\n')

#print("y_train_aux:", y_train_aux)

# Tengo de crear todas las máscaras de ground truth para las imágenes de entrenamiento que me faltan
# Cambiar el código para que se cojan los archivos de las subcarpetas de la carpeta dada en el entrenamiento y validación


# Load y_train with np.load
y_train = [np.load(fp).astype(np.int32) for fp in y_train_aux]

# Load X_train images using OpenCV
X_train = [cv2.imread(fp) for fp in X_train_paths]


"""
# Preparar datos de validación
ruta_carpeta_validacion = '../Imagenes_para_entrenamiento/IL6_1_solo_imagenes_y_ground_truth'


X_val_paths = []
guardar_elementos_de_carpeta(ruta_carpeta_validacion, X_val_paths, extension)
y_val_aux = []
guardar_elementos_de_carpeta(ruta_carpeta_validacion, y_val_aux, extension2)



#print("X_val_paths:", X_val_paths)
#print("y_val_aux:", y_val_aux)
"""


ruta_carpeta_validacion_def = '../Imagenes_validacion/'
path_resultado = []

X_val_paths = []

guardar_elementos_de_carpeta(ruta_carpeta_validacion_def, path_resultado, extension)
guardar_elementos_de_carpeta(ruta_carpeta_validacion_def, X_val_paths, extension)

y_val_aux = []

guardar_elementos_de_carpeta(ruta_carpeta_validacion_def, path_resultado, extension2)
guardar_elementos_de_carpeta(ruta_carpeta_validacion_def, y_val_aux, extension2)

#print("path_resultado:", path_resultado)
print("len(path_resultado):", len(path_resultado))

#exit()


# Load y_val with np.load
y_val = [np.load(fp).astype(np.int32) for fp in y_val_aux]

# Load X_val images using OpenCV
X_val = [cv2.imread(fp) for fp in X_val_paths]

del path_resultado, ruta_carpeta_validacion_def, ruta_carpeta_entrenamiento_def, extension, extension2
del X_train_paths, y_train_aux, X_val_paths, y_val_aux

# Configurar los parámetros de entrenamiento
channels = [0, 0]
normalize = True
weight_decay = 1e-4
learning_rate = 0.01
batch_size = 8 # Si acaso poner en 16 o en 32
num_epochs = 5000    # Reducido de 5000 a 1
nombre_modelo = 'mi_modelo_reentrenado_todas_las_imagenes_5000epochs'
destino_reentrenamiento = '../'
guardar_cada = 10 # Cada x epochs se guarda el modelo, por defecto es 100
min_train_masks = 1     # Reducido el valor de min_train_masks de 5 (por defecto) a 1, con esto ahora funciona

""" 26.571.644

# Verify and print the content and type of data before training
for i, label in enumerate(y_train):
    print(f"y_train[{i}]: type={type(label)}, shape={label.shape}, dtype={label.dtype}")
    print(f"Unique values in y_train[{i}]: {np.unique(label)}")

for i, label in enumerate(y_val):
    print(f"y_val[{i}]: type={type(label)}, shape={label.shape}, dtype={label.dtype}")
    print(f"Unique values in y_val[{i}]: {np.unique(label)}")

# Verify X_train elements are correct
for idx, img in enumerate(X_train):
    print(f"X_train element at index {idx}: {type(img)}, shape: {img.shape}, dtype={img.dtype}")

# Verify X_val elements are correct
for idx, img in enumerate(X_val):
    print(f"X_val element at index {idx}: {type(img)}, shape: {img.shape}, dtype={img.dtype}")

"""

#exit()

# Entrenar el modelo
model_path_all = train.train_seg(model.cp.net, train_data=X_train, train_labels=y_train,
                                 channels=channels, normalize=normalize, test_data=X_val, test_labels=y_val,
                                 weight_decay=weight_decay, SGD=True, learning_rate=learning_rate,
                                 batch_size=batch_size, n_epochs=num_epochs, model_name=nombre_modelo,
                                 save_path=destino_reentrenamiento, save_every=guardar_cada, min_train_masks=min_train_masks)

print("Modelo reentrenado y guardado en:", model_path_all)

exit()

#Tengo que revisar si de verdad se están pasando las máscaras porque creo que con las transformaciones que hago se va todo a la mierda.


# Mirar tamaño de imagen y tamaño de célula que se usa en el modelo
