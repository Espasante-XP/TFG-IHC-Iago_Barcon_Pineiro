#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time, os, sys
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import matplotlib as mpl
#get_ipython().run_line_magic('matplotlib', 'inline')  #No sé si está bien, esto sale de exportar a python la linea %matplotlib inline, con cualquiera de las 2 líneas me protesta
mpl.rcParams['figure.dpi'] = 300
from cellpose import utils, io

import matplotlib
matplotlib.use('TKAgg')     #Como no se puede ver nada con Qt, he mirado en internet y con este me iría     Source: https://stackoverflow.com/questions/41994485/how-to-fix-could-not-find-or-load-the-qt-platform-plugin-windows-while-using-m


#Añadido por mi para que carguen las imágenes de una carpeta
import os
from PIL import Image

# I will download images from website
#urls = ['http://www.cellpose.org/static/images/img02.png',
 #       'http://www.cellpose.org/static/images/img03.png',
  #      'http://www.cellpose.org/static/images/img05.png']

#files = ['./CellPose_test/test/000_img.png']
files = ['./Imagenes_para_entrenamiento/IL6_1/Image_1033.jpg']


imagenes = []

ruta_carpeta = '../Imagenes_para_entrenamiento/IL6_1'   #./Imagenes_para_entrenamiento/IL6_1

#C:\Users\iagob\OneDrive\Escritorio\Trabajo_TFG_local\TFG\Trabajo_TFG_actual\Imagenes para entrenamiento\IL6_1

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
  

"""
Creo que necesito cambiar todas las \ por / en las rutas de todas las imágenes porque si no me da un error.
"""

img2 = io.imread(imagenes[2])

plt.figure(figsize=(2,2))
plt.imshow(img2)
plt.axis('off')
plt.show()

#Prueba para generar solo una máscara y probar si se crea correctamente la imagen de la máscara

#Prueba para los cambios en diameter para probar con solo un elemento y que no esté ejecutando tanto tiempo

from cellpose import models, io

# DEFINE CELLPOSE MODEL
# model_type='cyto3' or model_type='nuclei'
model = models.Cellpose(gpu=False, model_type='cyto3')


channels = [[0,0]] #, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]

    
#for filename in imagenes:

filename = imagenes[2]

img2 = io.imread(imagenes[2]) #Pongo [2] por poner, es la imagen Image_1031.jpg
print(filename)

#import time
#time.sleep(75) # espera en segundos

# Utiliza siempre el primer valor de channels
chan = channels[0]

masks, flows, styles, diams = model.eval(img2, diameter=None, channels=chan)

# save results so you can load in gui
io.masks_flows_to_seg(img2, masks, flows, filename, channels=chan, diams=diams)

# save results as png
io.save_to_png(img2, masks, flows, filename)

"""
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


   ruta_carpeta = 'C:/Users/iagob/OneDrive/Escritorio/Trabajo_TFG_local/TFG/Trabajo_TFG_actual/Imagenes para entrenamiento/IL6_1'


imagen_mascara = 'C:/Users/iagob/OneDrive/Escritorio/Trabajo_TFG_local/TFG/Trabajo_TFG_actual/Imagenes para entrenamiento/IL6_1/Image_1034_cp_masks.png'

archivo_mascara = 'C:/Users/iagob/OneDrive/Escritorio/Trabajo_TFG_local/TFG/Trabajo_TFG_actual/Imagenes para entrenamiento/IL6_1/Image_1034_seg.npy'

import visualize_seg_mask

visualize_seg_mask(imagen_mascara, archivo_mascara)
"""
   
# DISPLAY RESULTS
from cellpose import plot

fig = plt.figure(figsize=(12,5))

plot.show_segmentation(fig, img2, masks, flows[0], channels=chan)
plt.tight_layout()
plt.show()



