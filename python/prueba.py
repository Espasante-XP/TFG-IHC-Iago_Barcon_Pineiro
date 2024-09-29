
import numpy as np

from generate_seg_mask import generate_seg_mask

imagen_mascara = '../Imagenes_para_entrenamiento/IL6_1/Image_1031_cp_masks.png'

archivo_mascara = '../Imagenes_para_entrenamiento/IL6_1/Image_1031_seg.npy'

imagenes = []

ruta_carpeta = '../Imagenes_para_entrenamiento/IL6_1'   #./Imagenes_para_entrenamiento/IL6_1

#C:\Users\iagob\OneDrive\Escritorio\Trabajo_TFG_local\TFG\Trabajo_TFG_actual\Imagenes para entrenamiento\IL6_1

import time, os, sys

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

textFile = imagenes[2]

last = textFile.rsplit(',', 1)[0]

#textFile = "example.txt"
fileName, _, extension = textFile.partition(".")
print(last)  # Output: example
#print(extension)  # Output: txt

def obtener_izquierda_delimitador(cadena, delimitador):
    # Encuentra la última ocurrencia del delimitador
    indice = cadena.rfind(delimitador)
    
    # Si el delimitador no se encuentra, devuelve la cadena completa
    if indice == -1:
        return cadena
    
    # Devuelve la parte de la cadena a la izquierda del delimitador
    return cadena[:indice]

# Ejemplo de uso
#cadena = "esto/es/un/ejemplo/de/uso"
cadena = imagenes[2]

#delimitador = "/"
delimitador = "."

resultado = obtener_izquierda_delimitador(cadena, delimitador)
print("Segunda función")
print(resultado)  # Salida: "esto/es/un/ejemplo/de"


# Cargar el archivo .npy como un array de numpy
mascara = np.load(archivo_mascara, allow_pickle=True) #Tengo que poner allow_pickle=True porque si no no me deja cargarlo

# Imprimir la forma del array para verificar sus dimensiones
print("máscara = ")
print(mascara.shape)



generate_seg_mask(imagen_mascara, mascara)

#Tengo que mirar de comprobar como de bien salen las máscaras con las métricas de cellpose, que por lo que veo no demasiado
