
from cellpose import utils
import numpy as np
import utils 
import cv2, os

def generate_seg_mask(image: np.ndarray, mask: np.ndarray, url: os.path):
   """
   Esta función toma una imagen y una máscara de segmentación, genera una imagen coloreada de la segmentación y la guarda en el disco.
    :param image: Input image as a numpy array.
    :param mask: Segmentation mask as a numpy array.
    :param url: URL where the generated segmentation mask will be saved.
   """
   color_seg = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
   palette = np.array(utils.create_ade20k_label_colormap()) 
   for label, color in enumerate(palette):
       color_seg[mask == label, :] = color
   color_seg = color_seg[..., ::-1]  # convert to BGR

   img = np.array(image) * 0.5 + color_seg * 0.5  # plot the image with the segmentation map
   img = img.astype(np.uint8)

   cv2.imwrite(url, img)


def obtener_izquierda_delimitador(cadena, delimitador):
    """
    Obtiene la parte de la cadena a la izquierda del último delimitador especificado.
    :param cadena: La cadena de texto de la que se extraerá la parte.
    :param delimitador: El delimitador que se usará para dividir la cadena.
    :return: La parte de la cadena a la izquierda del último delimitador.
    """
    # Encuentra la última ocurrencia del delimitador
    indice = cadena.rfind(delimitador)
    
    # Si el delimitador no se encuentra, devuelve la cadena completa
    if indice == -1:
        return cadena
    
    # Devuelve la parte de la cadena a la izquierda del delimitador
    return cadena[:indice]
