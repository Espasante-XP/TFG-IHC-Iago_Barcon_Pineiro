
import numpy as np
from pycocotools.coco import COCO
import os

def cargar_anotaciones_coco_de_archivo(annFile: os.path):
    coco=COCO(annFile) 

    image_ids = coco.getImgIds()

    mascaras_multietiqueta = []

    #Se crean las máscaras vacías, hay tantas imágenes (image_ids) como anotaciones (annotation_ids)
    for id in image_ids:
        img_info = coco.loadImgs(id)[0]
        height, width = img_info['height'], img_info['width']
        aux = np.zeros((height, width), dtype=np.uint8)
        mascaras_multietiqueta.append(aux)

    annotations = []
    index = 0

    for id in image_ids:
        annotation = coco.getAnnIds(imgIds=id)
        annotations = coco.loadAnns(annotation)
        for ann_index, annotation in enumerate(annotations):
            mask = coco.annToMask(annotation)                
            mascaras_multietiqueta[index][mask>0] = ann_index
        index = index + 1

    return coco, mascaras_multietiqueta
