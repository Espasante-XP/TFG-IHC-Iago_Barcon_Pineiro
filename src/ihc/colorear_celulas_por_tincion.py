
# -*- coding: utf-8 -*-

import numpy as np
import cv2, os
from typing import List

colores_tincion = {
    '1': [0, 0, 255],  # Azul
    '2': [0, 255, 0],        # Verde
    '3': [255, 255, 0],           # Amarillo
    '4': [255, 0, 0]   # Rojo
}

def tenhir_celulas_en_imagen(imagen: np.ndarray, celulas: np.ndarray, tincion_celula: List[int], nombre_img_resultante: os.path):

    """
    Aplica colores específicos a las células en una imagen según su tipo de tinción.

    Parámetros:
    - imagen (np.ndarray): Imagen original en formato BGR (como la devuelta por cv2.imread).
    - celulas (np.ndarray): Máscara de segmentación donde cada píxel representa una etiqueta de célula.
                          Las etiquetas deben ser enteros consecutivos empezando en 1.
    - tincion_celula (list[int]): Lista de enteros entre 1 y 4 que indica el tipo de tinción para cada célula.
                                 El orden debe corresponderse con el orden de las etiquetas (1, 2, 3...).
    - nombre_img_resultante (os.path): Ruta donde se guardará la imagen resultante.

    Excepciones:
    - ValueError: Si los valores de tincion_celula no están entre 1 y 4 o si el número de elementos en 
                  tincion_celula no coincide con el número de células etiquetadas.
    """

    # Comprobar que la imagen y la máscara tienen las mismas dimensiones
    if imagen.shape[:2] != celulas.shape[:2]:
        print("La imagen y la máscara deben tener las mismas dimensiones.")
        exit(1)

    # Contar el número de células etiquetadas (etiquetas únicas excluyendo el fondo 0)
    unique_labels = np.unique(celulas)
    if 0 in unique_labels:
        num_celulas = len(unique_labels) - 1  # Excluir el fondo (0)
    else:
        num_celulas = len(unique_labels)

    # Verificar que el número de tintes coincide con el número de células
    if len(tincion_celula) != num_celulas:
        print(f"El número de tintes ({len(tincion_celula)}) debe coincidir con el número de células etiquetadas ({num_celulas}).")
        exit(1)


    if not all(1 <= t <= 4 for t in tincion_celula):
        print("Los valores de tinción de las células deben estar entre 1 y 4.")
        exit(1)

    color_seg = np.zeros((celulas.shape[0], celulas.shape[1], 3), dtype=np.uint8)

    palette = np.array([colores_tincion[str(t)] for t in tincion_celula])

    for idx, color in enumerate(palette):
        label = idx + 1  # Etiquetas empiezan en 1
        color_seg[celulas == label, :] = color

    color_seg = color_seg[..., ::-1]  # Convertir a BGR

    img = (np.array(imagen) * 0.65 + color_seg * 0.35).astype(np.uint8)

    os.makedirs(os.path.dirname(nombre_img_resultante), exist_ok=True)
    
    cv2.imwrite(nombre_img_resultante, img)


