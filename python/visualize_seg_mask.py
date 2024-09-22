import matplotlib.pyplot as plt

from cellpose import utils, io

import numpy as np

import utils #creo que esto está mal, revisar

def visualize_seg_mask(image: np.ndarray, mask: np.ndarray):
   color_seg = np.zeros((mask.shape[0], mask.shape[1], 3), dtype=np.uint8)
   palette = np.array(utils.create_ade20k_label_colormap()) #Revisar, creo que no está bien
   for label, color in enumerate(palette):
       color_seg[mask == label, :] = color
   color_seg = color_seg[..., ::-1]  # convert to BGR

   img = np.array(image) * 0.5 + color_seg * 0.5  # plot the image with the segmentation map
   img = img.astype(np.uint8)

   plt.figure(figsize=(15, 10))
   plt.imshow(img)
   plt.axis("off")
   plt.show()

#Tengo que cambiar un par de cosas del final que dijo Raquel
