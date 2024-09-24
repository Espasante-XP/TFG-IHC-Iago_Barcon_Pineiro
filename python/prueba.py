
import numpy as np

from visualize_seg_mask import visualize_seg_mask

imagen_mascara = 'C:/Users/iagob/OneDrive/Escritorio/Trabajo_TFG_local/TFG/TFG-IHC-Iago_Barcon_Pineiro/Imagenes_para_entrenamiento/IL6_1/Image_1031_cp_masks.png'

archivo_mascara = '../Imagenes_para_entrenamiento/IL6_1/Image_1031_seg.npy'

#C:/Users/iagob/OneDrive/Escritorio/Trabajo_TFG_local/TFG/TFG-IHC-Iago_Barcon_Pineiro/Imagenes_para_entrenamiento/IL6_1/Image_1031_seg.npy

#C:\Users\iagob\OneDrive\Escritorio\Trabajo_TFG_local\TFG\TFG-IHC-Iago_Barcon_Pineiro\Imagenes para entrenamiento\IL6_1

# Cargar el archivo .npy como un array de numpy
mascara = np.load(archivo_mascara, allow_pickle=True) #Tengo que poner allow_pickle=True porque si no no me deja cargarlo

# Imprimir la forma del array para verificar sus dimensiones
print("máscara = ")
print(mascara.shape)

visualize_seg_mask(imagen_mascara, mascara)