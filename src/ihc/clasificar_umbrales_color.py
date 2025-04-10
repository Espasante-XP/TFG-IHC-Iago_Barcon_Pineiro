
from cargar_anotaciones import cargar_anotaciones_coco_de_archivo
from pycocotools.coco import COCO
from collections import defaultdict
from utils import obter_lista_ficheiros
import os, shutil, gc


# Hacer un código que en base a los valores que hay de todas las imágenes, pille las tinciones de las anotaciones
# Con las tinciones de las anotaciones se seleccionan las células que tienen cada tipo de tinción
# Se hace una gráfica de las células que tienen cada tipo de tinción mirando máximo, mínimo, media, mediana y posibles outliers (los hay mínimo en FNB 4_3) de cada tinción para ver si hay un umbral


carpetas_clasificacion = ["sin tincion", "minima", "media", "maxima"]

carpetas_datos = ["HSV", "RGB", "LAB"]

dir_general = "../../valores_comp_conexas/"

dir_nuevo_general = "../../valores_clasif_tincion"

dir_anotaciones_coco_general = "./anotaciones_coco_v2"


def obtener_indices_por_categoria(fuentes):
    """
    Devuelve índices de anotaciones agrupados por category_id y el conjunto completo de anotaciones.
    
    Args:
        fuentes (str/list): Ruta(s) a archivo(s) JSON o lista(s) de anotaciones.
        
    Returns:
        tuple: 
            - Lista de category_id únicos ordenados
            - Lista de listas de índices (posiciones) en el conjunto combinado
            - Lista de todas las anotaciones combinadas
    """
    combined_annotations = []
    
    # Convertir entrada en lista si es un solo elemento
    if not isinstance(fuentes, list):
        fuentes = [fuentes]
    
    # Cargar todas las anotaciones
    for fuente in fuentes:
        if isinstance(fuente, str):
            coco = COCO(fuente)
            combined_annotations.extend(coco.dataset['annotations'])
        elif isinstance(fuente, list):
            combined_annotations.extend(fuente)
        else:
            raise TypeError(f"Tipo no soportado: {type(fuente)}")
    
    # Crear grupos de índices por categoría
    groups = defaultdict(list)
    for idx, ann in enumerate(combined_annotations):
        groups[ann['category_id']].append(idx)
    
    # Preparar resultados ordenados
    category_ids = sorted(groups.keys())
    indices_per_category = [groups[cat_id] for cat_id in category_ids]
    
    return category_ids, indices_per_category, combined_annotations





dir_HSV = os.path.join(dir_general, carpetas_datos[0])

lista_carpetas = []

# Obtengo la lista de carpetas de imagenes -> Control_negativo_1', 'Control_negativo_2' ...
for carpeta in os.listdir(dir_HSV):
    if os.path.isdir(os.path.join(dir_HSV, carpeta)):
        lista_carpetas.append(carpeta)



lista_anotaciones_coco = []

# Obtengo la lista de anotaciones COCO de cada carpeta de imagenes
for directorio in lista_carpetas:
    aux = os.path.join(dir_anotaciones_coco_general, directorio)
    lista_anotaciones_coco.append(obter_lista_ficheiros(aux, ".json"))

# Lista con los 3 directorios de datos de las componentes conexas
lista_dir_datos = []

for dir in carpetas_datos:
    lista_dir_datos.append(os.path.join(dir_general, dir))

# Lista con los 12 directorios de datos de las tinciones, 4 por cada tipo de componente conexa (HSV, RGB y LAB)
# ../../valores_clasif_tincion/HSV/sin tincion, ./../valores_clasif_tincion/HSV/minima, ./../valores_clasif_tincion/HSV/media, etc
lista_dir_nuevos_datos = []

for dir in carpetas_clasificacion:
    for dir_datos in carpetas_datos:
        lista_dir_nuevos_datos.append(os.path.join(dir_nuevo_general, dir_datos, dir))

#print("lista_dir_nuevos_datos: ", lista_dir_nuevos_datos)

for dir_nuevo in lista_dir_nuevos_datos:
        if not os.path.exists(dir_nuevo):
            os.makedirs(dir_nuevo) # Mirar de poner el flag de que si no existe se cree para que sea más eficiente

print("lista_dir_nuevos_datos: ", lista_dir_nuevos_datos)




gc.collect() 

""" 
pos_datos = 0

pos_anotacion = 0
for anotaciones_coco in lista_anotaciones_coco:

    if(buscar_secuencia_en_path(anotaciones_coco[0], "Control_negativo_3", False)):
        print("anotaciones_coco: ", anotaciones_coco)
        print("pos_datos: ", pos_datos)
        print("pos_anotacion: ", pos_anotacion)
        #exit()
    else:
        print("anotaciones_coco: ", anotaciones_coco)
        
        directorio_datos = []

        directorio_datos = os.path.join(dir_general, carpetas_datos[pos_datos], lista_carpetas[pos_anotacion])

        #for dir_datos in lista_dir_datos:
        #    directorio_datos.append(os.path.join(dir_datos, lista_carpetas[pos_anotacion]))

        archivos_json = []
        archivos_json = obter_lista_ficheiros(directorio_datos, ".json")

        #print("archivos_json: ", archivos_json)
        #print("len(archivos_json): ", len(archivos_json))
        #exit()

        dir_nuevos_valores = []

        for dir in carpetas_clasificacion:
            dir_nuevos_valores.append(os.path.join(dir_nuevo_general, carpetas_datos[pos_datos], dir, lista_carpetas[pos_anotacion]))


        print("dir_nuevos_valores: ", dir_nuevos_valores)
        
        for dir_nuevo in dir_nuevos_valores:
            if not os.path.exists(dir_nuevo):
                os.makedirs(dir_nuevo)
        #exit()
        #lista_archivos_json = []

        #for dir_datos in directorio_datos:
        #    lista_archivos_json.append(obter_lista_ficheiros(dir_datos, ".json"))

        #print("len(lista_archivos_json): ", len(lista_archivos_json))
        #print("lista_archivos_json[0]: ", lista_archivos_json[0])
        #exit()
        #print("archivos_json: ", archivos_json)
        #print("len(archivos_json): ", len(archivos_json))
        #dir_anotaciones_coco = "./anotaciones_coco_enviadas/IL6_1/IL6_1_coco.json"
        #lista_category, lista_indices, _ = obtener_indices_por_categoria(dir_anotaciones_coco)

        _, lista_indices, _ = obtener_indices_por_categoria(anotaciones_coco)


        #lista_archivos_categoria = []
        #for indices in lista_indices:
        #    lista_aux = []
        #    for indice in indices:
        #        aux = archivos_json[indice]
        #        lista_aux.append(aux)
        #    lista_archivos_categoria.append(lista_aux)


        lista_archivos_categoria = []
        
        for indices in lista_indices:
            lista_aux = []
            
            print("len(archivos_json): ", len(archivos_json))
            print("indices: ", indices)

            #print("archivos_json: ", archivos_json)
            #print("indices: ", indices)
            for indice in indices:
                #if indice == 308 and buscar_secuencia_en_path(aux, "Control_negativo_3", False):
                    #print("aux: ", aux)
                #else:
                
                aux = archivos_json[indice]
                lista_aux.append(aux)
                #if(buscar_secuencia_en_path(aux, "IL6_1", False)):
                #    print("aux: ", aux)
                #    print("indice: ", indice)
                #    print("len(archivos_json): ", len(archivos_json))
                #    print("archivos_json[indice]: ", archivos_json[indice])
                #    exit()
                #print("aux: ", aux)
                #exit()
            lista_archivos_categoria.append(lista_aux)

        #print("len(lista_archivos_categoria): ", len(lista_archivos_categoria))

        #exit()
        
        
        n = 0
        for listas in lista_archivos_categoria:

            for lista in listas:

                #print("lista: ", lista)
                #exit()

                carpeta_imagen = os.path.basename(os.path.dirname(os.path.dirname(lista)))

                #print("carpeta_imagen: ", carpeta_imagen)

                carpeta_archivo = os.path.splitext(os.path.basename(os.path.dirname(lista)))[0]
                #print("carpeta_archivo: ", carpeta_archivo)
                
                #nuevo_nombre_archivo = os.path.join(dir_nuevos_valores[n], carpeta_archivo)
                #aux = os.path.join(dir_nuevo_general, dir_datos)

                nuevo_nombre_archivo = os.path.join(dir_nuevo_general, carpetas_datos[pos_datos], carpetas_clasificacion[n], carpeta_imagen, carpeta_archivo)

                #print("dir_nuevo_general: ", dir_nuevo_general)
                #print("carpetas_datos[pos_datos]: ", carpetas_datos[pos_datos])
                #print("carpetas_clasificacion[n]: ", carpetas_clasificacion[n])
                #print("carpeta_imagen: ", carpeta_imagen)
                #print("carpeta_archivo: ", carpeta_archivo)

                #print("nuevo_nombre_archivo: ", nuevo_nombre_archivo)

                

                if not os.path.exists(nuevo_nombre_archivo):
                    os.makedirs(nuevo_nombre_archivo)

                shutil.copy(lista, nuevo_nombre_archivo)

                #exit()
                
            n = n + 1
            #exit()    
            
            #cosa = 1   
                

        #exit()


        pos_anotacion = pos_anotacion + 1

"""


#Viejo, no acaba de ir
pos_anotacion = 0
for anotaciones_coco in lista_anotaciones_coco:
    
    directorio_datos = []

    #directorio_datos = "../../valores_comp_conexas/HSV/IL6_1"
    #directorio_datos = os.path.join(dir_general, carpetas_datos[0], lista_carpetas[pos_anotacion])

    for dir_datos in lista_dir_datos:
        directorio_datos.append(os.path.join(dir_datos, lista_carpetas[pos_anotacion]))

    #archivos_json = []
    #archivos_json = obter_lista_ficheiros(directorio_datos, ".json")

    lista_archivos_json = []

    for dir_datos in directorio_datos:
        lista_archivos_json.append(obter_lista_ficheiros(dir_datos, ".json"))


    #dir_anotaciones_coco = "./anotaciones_coco_enviadas/IL6_1/IL6_1_coco.json"
    #lista_category, lista_indices, _ = obtener_indices_por_categoria(dir_anotaciones_coco)


    # El código base que funciona
    #_, lista_indices, _ = obtener_indices_por_categoria(anotaciones_coco)

    #print("len(lista_indices): ", len(lista_indices))
    #exit()

    # Obtener índices por categoría (debe devolver 4 grupos)
    _, lista_indices, _ = obtener_indices_por_categoria(anotaciones_coco)
    
    # Validar que hay 4 categorías (tengo que darle una vuelta)
    if len(lista_indices) != 4:
        raise ValueError(f"Se esperaban 4 categorías, pero se encontraron {len(lista_indices)}")

    # Procesar cada categoría (sin anidar con tipos de datos)
    lista_archivos_categoria = []
    for categoria_idx, indices in enumerate(lista_indices):
        # Recoger archivos de todos los tipos (HSV, RGB, LAB)
        archivos_por_tipo = []
        for archivos_json in lista_archivos_json:
            # Verificar índices para este tipo de datos
            archivos_validos = []
            for idx in indices:
                if idx < len(archivos_json):
                    archivos_validos.append(archivos_json[idx])
                else:
                    print(f"Índice {idx} fuera de rango en {archivos_json}")
            archivos_por_tipo.append(archivos_validos)
        
        # Agregar a la categoría actual
        lista_archivos_categoria.append(archivos_por_tipo)


    """ """
    lista_archivos_categoria = []
    lista_listas_archivos_categoria = []

    
    i = 0
    for indices in lista_indices:
        print("len(lista_indices): ", len(lista_indices))
        print("lista_indices: ", lista_indices)
        for archivos_json in lista_archivos_json:
            lista_aux = []
            print("len(archivos_json): ", len(archivos_json))
            print("indices: ", indices)
            #print("anotaciones_coco: ", anotaciones_coco)
            for indice in indices:
                aux = archivos_json[indice]
                lista_aux.append(aux)
            lista_archivos_categoria.append(lista_aux)
            i = i + 1
        print("len(lista_archivos_json): ", len(lista_archivos_json))
        print("len(lista_archivos_categoria): ", len(lista_archivos_categoria))    
        lista_listas_archivos_categoria.append(lista_archivos_categoria)
    


    
    """ """
    for lista_archivos_categoria in lista_listas_archivos_categoria:
        #print("lista_archivos_categoria[0]: ", lista_archivos_categoria[0])
        n = 0
        for listas in lista_archivos_categoria:
            print("type(listas[0]): ", type(listas[0]))
            print("len(listas): ", len(listas))
            #print("listas: ", listas)
            print("len(lista_archivos_categoria): ", len(lista_archivos_categoria)) # Tiene que dar 12
            #print(lista_archivos_categoria)
            for lista in listas:

                #print("lista: ", lista)

                carpeta_imagen = os.path.basename(os.path.dirname(os.path.dirname(lista)))

                #print("carpeta_imagen: ", carpeta_imagen)

                carpeta_archivo = os.path.splitext(os.path.basename(os.path.dirname(lista)))[0]
                #print("carpeta_archivo: ", carpeta_archivo)
                
                #nuevo_nombre_archivo = os.path.join(dir_nuevos_valores[n], carpeta_archivo)
                #aux = os.path.join(dir_nuevo_general, dir_datos)

                nuevo_nombre_archivo = os.path.join(lista_dir_nuevos_datos[n], carpeta_imagen, carpeta_archivo)

                #print("lista_dir_nuevos_datos[n]: ", lista_dir_nuevos_datos[n])

                #print("nuevo_nombre_archivo: ", nuevo_nombre_archivo)

                #exit()

                if not os.path.exists(nuevo_nombre_archivo):
                    os.makedirs(nuevo_nombre_archivo)

                #print("lista: ", lista)
                #print("nuevo_nombre_archivo: ", nuevo_nombre_archivo)

                shutil.copy(lista, nuevo_nombre_archivo)

            print("nuevo_nombre_archivo: ", nuevo_nombre_archivo)
            n = n + 1
        
            

    #exit()


    pos_anotacion = pos_anotacion + 1
    gc.collect() 



