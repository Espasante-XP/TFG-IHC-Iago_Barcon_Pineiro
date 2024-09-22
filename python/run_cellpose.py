#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import time, os, sys
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import matplotlib as mpl
get_ipython().run_line_magic('matplotlib', 'inline')  #No sé si está bien
mpl.rcParams['figure.dpi'] = 300
from cellpose import utils, io

#Añadido por mi para que carguen las imágenes de una carpeta
import os
from PIL import Image

# I will download images from website
#urls = ['http://www.cellpose.org/static/images/img02.png',
 #       'http://www.cellpose.org/static/images/img03.png',
  #      'http://www.cellpose.org/static/images/img05.png']

#files = ['./CellPose_test/test/000_img.png']
files = ['./Imagenes_para_entrenamiento/IL6_1/Image_1033.jpg']


"""
#Lo saqué de Bing
import os
from PIL import Image

def cargar_imagenes(ruta_carpeta):
    imagenes = []
    for nombre_archivo in os.listdir(ruta_carpeta):
        if nombre_archivo.endswith('.jpg') or nombre_archivo.endswith('.png'):  # Asegúrate de poner aquí todos los formatos que quieras cargar
            ruta_imagen = os.path.join(ruta_carpeta, nombre_archivo)
            imagen = Image.open(ruta_imagen)
            imagenes.append(imagen)
    return imagenes

# Uso de la función
imagenes = cargar_imagenes('ruta/a/tu/carpeta')
"""

imagenes = []

ruta_carpeta = './Imagenes_para_entrenamiento/IL6_1'

#i = 0
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
  
#for url in urls:
 #   parts = urlparse(url)
  #  filename = os.path.basename(parts.path)
   # if not os.path.exists(filename):
    #    sys.stderr.write('Downloading: "{}" to {}\n'.format(url, filename))
     #   utils.download_url_to_file(url, filename)
    #files.append(filename)

# REPLACE FILES WITH YOUR IMAGE PATHS
# files = ['img0.tif', 'img1.tif']

# view 1 image
#img = io.imread(files[-1])

#Añadido por mi tras mirar en Bing
#img = img / np.amax(img)
#plt.imshow(tu_imagen)

img2 = io.imread(imagenes[2])


#img2 = img2 / np.amax(img2)


#plt.figure(figsize=(2,2))
#plt.imshow(img)
#plt.axis('off')
#plt.show()

plt.figure(figsize=(2,2))
plt.imshow(img2)
plt.axis('off')
plt.show()


# In[2]:


print(imagenes)


# In[2]:


# RUN CELLPOSE

from cellpose import models, io

# DEFINE CELLPOSE MODEL
# model_type='cyto3' or model_type='nuclei'
model = models.Cellpose(gpu=False, model_type='cyto3')

# define CHANNELS to run segementation on
# grayscale=0, R=1, G=2, B=3
# channels = [cytoplasm, nucleus]
# if NUCLEUS channel does not exist, set the second channel to 0
# channels = [0,0]
# IF ALL YOUR IMAGES ARE THE SAME TYPE, you can give a list with 2 elements
# channels = [0,0] # IF YOU HAVE GRAYSCALE
# channels = [2,3] # IF YOU HAVE G=cytoplasm and B=nucleus
# channels = [2,1] # IF YOU HAVE G=cytoplasm and R=nucleus

# or if you have different types of channels in each image
#channels = [[2,3], [0,0], [0,0]]

channels = [[0,0]] #, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]

# He quitado todos los canales menos uno, a ver si aún así saca todas las máscaras

# if diameter is set to None, the size of the cells is estimated on a per image basis
# you can set the average cell `diameter` in pixels yourself (recommended) 
# diameter can be a list or a single number for all images

# you can run all in a list e.g.
# >>> imgs = [io.imread(filename) in for filename in files]
# >>> masks, flows, styles, diams = model.eval(imgs, diameter=None, channels=channels)
# >>> io.masks_flows_to_seg(imgs, masks, flows, diams, files, channels)
# >>> io.save_to_png(imgs, masks, flows, files)

# or in a loop
#for chan, filename in zip(channels, files): #files es del viejo donde solo se usa la 33
#for chan, filename in zip(channels, imagenes):
    
    #img2 = io.imread(filename) #Cambié img por img2
    #print(filename)
    
    #masks, flows, styles, diams = model.eval(img2, diameter=None, channels=chan)

    # save results so you can load in gui
    #io.masks_flows_to_seg(img2, masks, flows, filename, channels=chan, diams=diams)

    # save results as png
    #io.save_to_png(img2, masks, flows, filename)
    
for filename in imagenes:
    img2 = io.imread(filename)  # Cambié img por img2
    #print(filename)
    
    # Utiliza siempre el primer valor de channels
    chan = channels[0]

    masks, flows, styles, diams = model.eval(img2, diameter=None, channels=chan)

    # save results so you can load in gui
    io.masks_flows_to_seg(img2, masks, flows, filename, channels=chan, diams=diams)

    # save results as png
    io.save_to_png(img2, masks, flows, filename)
    


# In[2]:


#Prueba para los cambios en diameter para probar con solo un elemento y que no esté ejecutando tanto tiempo

from cellpose import models, io

# DEFINE CELLPOSE MODEL
# model_type='cyto3' or model_type='nuclei'
model = models.Cellpose(gpu=False, model_type='cyto3')


channels = [[0,0]] #, [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0], [0,0]

    
#for filename in imagenes:

filename = imagenes[2]

img2 = io.imread(imagenes[2]) #Pongo [2] por poner
print(filename)

# Utiliza siempre el primer valor de channels
chan = channels[0]

masks, flows, styles, diams = model.eval(img2, diameter=None, channels=chan)

# save results so you can load in gui
io.masks_flows_to_seg(img2, masks, flows, filename, channels=chan, diams=diams)

# save results as png
io.save_to_png(img2, masks, flows, filename)



# In[6]:


#Ya va para generar fotos, ahora tengo que ver como puedo pasarle la variable masks para que me la ponga bien

import cv2

import numpy as np

#im = cv2.imread('./Imagenes_para_entrenamiento/IL6_1/Image_1037.jpg')

im = cv2.imread(masks)

#cv2.imshow('Prueba cv2', im)

# Cargar la imagen desde el archivo NPY
#imagenPrueba = np.load('./Imagenes_para_entrenamiento/IL6_1/Image_1037_seg.npy')


#imagenPrueba = './Imagenes_para_entrenamiento/IL6_1/Image_1037_seg.npy'

cv2.imwrite('pruebaNPYImagen1037.png', im) #flows


# In[1]:


import subprocess

resultado = subprocess.run(['ls','-l'], capture_output=True, text=True)

print(resultado)

#subprocess.run([""])


subprocess.run(['/usr/bin/gnome-terminal'])


# In[26]:


from PIL import Image
import numpy as np

# Supongamos que masks es una matriz de imagen (numpy.ndarray)
# Conviértela en una imagen de Pillow
img_pil = Image.fromarray(masks)

img_pil.save("nueva_imagen.jpg")

# Ahora puedes abrir la imagen
#im = img_pil.open()


# In[25]:


from PIL import Image
import numpy as np

# Supongamos que masks es una matriz de imagen (numpy.ndarray)
# Conviértela en una imagen de Pillow
img_pil = Image.fromarray(masks)

print(img_pil)

# Ahora puedes abrir la imagen
im = img_pil.open()


# In[20]:


from PIL import Image

# Cargar la imagen
im = Image.open(masks)


# In[9]:


import numpy as np

b = np.asarray(masks)

for i in (b.shape[1]):
    print(b[0,i])


# In[5]:


print('Mask = ')

print(type(masks))

print(masks)

print('Flows = ')

print(type(flows))

print(flows)

print('Img2 = ')

print(type(img2))

print(img2)

print('Filename = ')

print(type(filename))

print(filename)


# In[11]:


# DISPLAY RESULTS
from cellpose import plot

fig = plt.figure(figsize=(12,5))

#Añadido por mi tras mirar en Bing
#img = img / np.amax(img)
#plt.imshow(tu_imagen)

plot.show_segmentation(fig, img2, masks, flows[0], channels=chan)
plt.tight_layout()
plt.show()


# In[ ]:


# DISPLAY RESULTS
from cellpose import plot

fig = plt.figure(figsize=(12,5))

plot.show_segmentation(fig, imgs, masks, flows[0], channels=chan)
plt.tight_layout()
plt.show()


# In[ ]:





# In[ ]:





# In[12]:


#from cellpose.tests import test_output

#from tests import test_output


#./Imagenes_para_entrenamiento/IL6_1/Image_1037_seg.npy
#./Imagenes_para_entrenamiento/IL6_1/Image_1037.jpg
#
#model_type='cyto3'

#masks, flows, styles, diams    /tests


from copia_codigo_base.cellpose.tests import test_output

from pathlib import Path #Para que se use la función joinpath

data_dir = './Imagenes_para_entrenamiento/IL6_1/Image_1037_seg.npy'

image_names = './Imagenes_para_entrenamiento/IL6_1/Image_1037.jpg'

runtype = '2D'

model_type = 'cyto3'

test_output.compare_masks(data_dir, image_names, runtype, model_type)


# In[ ]:





# In[ ]:




