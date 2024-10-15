import matplotlib.pyplot as plt

from cellpose import utils, io

import numpy as np

import utils #creo que esto está mal, revisar

import cv2, os

def generate_seg_mask(image: np.ndarray, mask: np.ndarray, url: os.path):
   color_seg = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
   palette = np.array(utils.create_ade20k_label_colormap()) #Revisar, creo que no está bien
   for label, color in enumerate(palette):
       color_seg[mask == label, :] = color
   color_seg = color_seg[..., ::-1]  # convert to BGR

   img = np.array(image) * 0.5 + color_seg * 0.5  # plot the image with the segmentation map
   img = img.astype(np.uint8)

   cv2.imwrite(url, img) #Creo que está mal

   #plt.figure(figsize=(15, 10))
   #plt.imshow(img)
   #plt.axis("off")
   #plt.show()


def obtener_izquierda_delimitador(cadena, delimitador):
    # Encuentra la última ocurrencia del delimitador
    indice = cadena.rfind(delimitador)
    
    # Si el delimitador no se encuentra, devuelve la cadena completa
    if indice == -1:
        return cadena
    
    # Devuelve la parte de la cadena a la izquierda del delimitador
    return cadena[:indice]
