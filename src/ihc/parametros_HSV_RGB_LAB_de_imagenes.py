
import cv2
import os
import numpy as np
from utils import obter_lista_ficheiros
import json

dir_resultados_base = "../../parametros_HSV_RGB_LAB/"


def crear_dir_resultados(carpeta_guardar_resultados=None):
    return os.path.join(dir_resultados_base, carpeta_guardar_resultados)

def create_path_new_folder(directory_path, carpeta_guardar_resultados):

    dir_resultados = crear_dir_resultados(carpeta_guardar_resultados)
    # Extraer el nombre del archivo y su directorio
    nombre_imagen = os.path.basename(directory_path)  # Nombre del archivo (con extensión)
    directorio_imagen = os.path.dirname(directory_path)  # Directorio completo donde está la imagen
    
    # Obtener el nombre del directorio final
    folder_name = os.path.basename(directorio_imagen)
    
    # Eliminar la extensión del nombre de la imagen
    nombre_imagen_sin_extension, _ = os.path.splitext(nombre_imagen)
    
    # Crear la ruta completa para la nueva carpeta dentro de path_folder_metrics
    metrics_folder_path = os.path.join(dir_resultados, folder_name)
    
    # Asegurarse de que la carpeta exista, si no, crearla
    os.makedirs(metrics_folder_path, exist_ok=True)

    full_path = os.path.join(metrics_folder_path, nombre_imagen_sin_extension)

    return full_path

# Comprobar si la imagen y la máscara existen, si tienen las mismas dimensiones y si se pueden leer/cargar correctamente
def comprobar_imagenes_y_mascaras_correcta(image_path, mask_path):
    error = False
    # Leer la imagen y la máscara
    if not os.path.exists(image_path):
        print(f"Imagen no encontrada: {image_path}")
        return None, None, True

    if not os.path.exists(mask_path):
        print(f"Máscara no encontrada: {mask_path}")
        return None, None, True

    image = cv2.imread(image_path)
    if image is None:
        print(f"Error al leer: {image_path}")
        return None, None, True
    
    try:
        mask = np.load(mask_path)
    except Exception as e:
        print(f"Error al cargar máscara {mask_path}: {e}")
        return None, None, True
    
    if image.shape[:2] != mask.shape:
        print(f"Error: Dimensiones no coinciden en {image_path}")
        return None, None, True
    return image, mask, error


# Esta función calcula la distancia de Mahalanobis entre un píxel y el modelo gaussiano del fondo
def calcular_distancia_mahalanobis(matrix, image, mask): 
    error = False
    # Modelo gaussiano del fondo (en RGB)
    background_pixels = matrix[mask == 0].T  # Píxeles de fondo (label == 0) 
    if background_pixels.size == 0:
        return None, True
    
    bg_mean = np.mean(background_pixels, axis=1)
    cov_matrix = np.cov(background_pixels)
    
    # Inversa de la matriz de covarianza (manejo de errores)
    try:
        inv_bg_cov = np.linalg.inv(cov_matrix)
    except np.linalg.LinAlgError:
        inv_bg_cov = np.linalg.pinv(cov_matrix)  # Pseudoinversa si es singular
    
    # Cálculo de la distancia de Mahalanobis para cada píxel (en RGB)
    distances = np.zeros(image.shape[:2])
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            pixel_rgb = matrix[i, j] # rgb_image
            diff = pixel_rgb - bg_mean
            dist = np.sqrt(np.dot(diff.T, np.dot(inv_bg_cov, diff)))
            distances[i, j] = dist
    return distances, error


def crear_dir_y_subdir_resultados(image_path, carpeta_guardar_resultados):

    path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) 
    base_name = os.path.basename(path_valores)

    if not os.path.exists(path_valores):
        os.makedirs(path_valores, exist_ok=True)

    return base_name, path_valores


def filtrado_zscore(zscore, threshold_zscore):
    thresholded_pixels = zscore > threshold_zscore # esto ya es parte de la clasificación de la tinción, por tanto, no se tiene que hacer
    filtered_zscore = zscore[thresholded_pixels]
    return filtered_zscore


def clasificar_tincion(zscore, area_tincion, threshold_no_tincion, threshold_min, threshold_max, threshold_max_area):
    # tengo que meter aquí el filtrado ese que hago arriba que no es necesario y se tiene que implementar aquí
    """
    if ((len(zscore) == 0) or max(zscore) == 0.0):
        nivel_tincion = "sin tincion" 
    elif np.median(zscore) < np.percentile(zscore, threshold_min):
        nivel_tincion = "minima"
    elif np.median(zscore) < np.percentile(zscore, threshold_max):
        nivel_tincion = "media"
    elif np.median(zscore) >= np.percentile(zscore, threshold_max):
        if area_tincion > threshold_max_area:
            nivel_tincion = "maxima"
        else:
            nivel_tincion = "media"
    """

    if (max(zscore) < threshold_no_tincion):
        nivel_tincion = "sin tincion"
    elif max(zscore) >= threshold_no_tincion and max(zscore) < threshold_min:
        nivel_tincion = "minima"
    elif max(zscore) >= threshold_min and max(zscore) < threshold_max  :
        nivel_tincion = "media"
    elif max(zscore) >= threshold_max:
        if area_tincion > threshold_max_area:
            nivel_tincion = "maxima"
        else:
            nivel_tincion = "media"
    return nivel_tincion


# Genera un archivo json de los valores HSV de cada célula anotada en una imagen en base a las máscara de los archivos NPY
def obtener_datos_HSV_de_imagenes(image_paths, mask_paths):
    if len(image_paths) != len(mask_paths):
        raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
    
    for image_path, mask_path in zip(image_paths, mask_paths):

        print("Analizando la imagen: ", image_path)

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue
        
        try:
            mask = np.load(mask_path)
        except Exception as e:
            print(f"Error al cargar máscara {mask_path}: {e}")
            continue
        
        if image.shape[:2] != mask.shape:
            print(f"Error: Dimensiones no coinciden en {image_path}")
            continue
        
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        
        
        carpeta_guardar_resultados = "HSV"

        path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)

        save_data_paths = os.path.join(save_data_paths, base_name)

        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)

        
        # Procesar cada célula en la máscara
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            
            # Extraer valores HSV para esta célula
            h = hsv_image[..., 0][component_mask != 0].tolist()
            s = hsv_image[..., 1][component_mask != 0].tolist()
            v = hsv_image[..., 2][component_mask != 0].tolist()
            
            # Calcular promedios para esta célula
            mean_h = float(np.median(h)) if h else 0.0
            mean_s = float(np.median(s)) if s else 0.0
            mean_v = float(np.median(v)) if v else 0.0
            

            filename = f"{base_name}_cell_{label}"

            # Guardar JSON
            data = {
                "h_all": h,
                "s_all": s,
                "v_all": v,
                "mean_h": mean_h,
                "mean_s": mean_s,
                "mean_v": mean_v
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")


# Genera un archivo json de los valores RGB de cada célula anotada en una imagen en base a las máscara de los archivos NPY
def obtener_datos_RGB_de_imagenes(image_paths, mask_paths):
    if len(image_paths) != len(mask_paths):
        raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
    
    for image_path, mask_path in zip(image_paths, mask_paths):

        print("Analizando la imagen: ", image_path)

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue
        
        try:
            mask = np.load(mask_path)
        except Exception as e:
            print(f"Error al cargar máscara {mask_path}: {e}")
            continue
        
        if image.shape[:2] != mask.shape:
            print(f"Error: Dimensiones no coinciden en {image_path}")
            continue
        
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        

        carpeta_guardar_resultados = "RGB"

        path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)

        save_data_paths = os.path.join(save_data_paths, base_name)

        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)

        
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            
            # Extraer valores RGB para esta célula
            r = rgb_image[..., 0][component_mask != 0].tolist()
            g = rgb_image[..., 1][component_mask != 0].tolist()
            b = rgb_image[..., 2][component_mask != 0].tolist()
            
            # Calcular promedios
            mean_r = float(np.median(r)) if r else 0.0
            mean_g = float(np.median(g)) if g else 0.0
            mean_b = float(np.median(b)) if b else 0.0
          
            filename = f"{base_name}_cell_{label}"

            # Guardar JSON
            data = {
                "r_all": r,
                "g_all": g,
                "b_all": b,
                "mean_r": mean_r,
                "mean_g": mean_g,
                "mean_b": mean_b
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")


# Genera un archivo json de los valores LAB de cada célula anotada en una imagen en base a las máscara de los archivos NPY
def obtener_datos_LAB_de_imagenes(image_paths, mask_paths):
    if len(image_paths) != len(mask_paths):
        raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")

    for image_path, mask_path in zip(image_paths, mask_paths):
        print("Analizando la imagen: ", image_path)

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue

        try:
            mask = np.load(mask_path)
        except Exception as e:
            print(f"Error al cargar máscara {mask_path}: {e}")
            continue

        if image.shape[:2] != mask.shape:
            print(f"Error: Dimensiones no coinciden en {image_path}")
            continue

        # Convertir a espacio de color LAB
        lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]

        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue

        carpeta_guardar_resultados = "LAB"

        path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json
    
        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)

        save_data_paths = os.path.join(save_data_paths, base_name)

        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)

        # Procesar cada célula en la máscara
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)

            # Extraer valores LAB para esta célula
            l = lab_image[..., 0][component_mask != 0].tolist()
            a = lab_image[..., 1][component_mask != 0].tolist()
            b = lab_image[..., 2][component_mask != 0].tolist()

            # Calcular promedios para esta célula
            mean_l = float(np.median(l)) if l else 0.0
            mean_a = float(np.median(a)) if a else 0.0
            mean_b = float(np.median(b)) if b else 0.0

            filename = f"{base_name}_cell_{label}"

            # Guardar JSON
            data = {
                "l_all": l,
                "a_all": a,
                "b_all": b,
                "mean_l": mean_l,
                "mean_a": mean_a,
                "mean_b": mean_b
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        if(save_data_paths == "../../parametros_HSV_RGB_LAB/LAB\Control_negativo_1\Image_1004\Image_1004_cell_15.json"):
            exit(0)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")


# Genera un archivo json de los valores HSV de cada célula anotada en una imagen en base a las máscara de los archivos NPY
# Se realiza normalizado CLAHE en el canal V
def obtener_datos_HSV_de_imagenes_clahe(image_paths, mask_paths):
    if len(image_paths) != len(mask_paths):
        raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
    
    for image_path, mask_path in zip(image_paths, mask_paths):
        print("Analizando la imagen: ", image_path)
        
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue
        
        try:
            mask = np.load(mask_path)
        except Exception as e:
            print(f"Error al cargar máscara {mask_path}: {e}")
            continue
        
        if image.shape[:2] != mask.shape:
            print(f"Error: Dimensiones no coinciden en {image_path}")
            continue
        
        # Convertir a HSV y aplicar CLAHE al canal V
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv_image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        v_clahe = clahe.apply(v)
        hsv_image_clahe = cv2.merge([h, s, v_clahe])
        
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        

        carpeta_guardar_resultados = "HSV_CLAHE"

        path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)
        save_data_paths = os.path.join(save_data_paths, base_name)
        
        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)
        
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            
            # Extraer valores HSV con CLAHE aplicado
            h_values = hsv_image_clahe[..., 0][component_mask != 0].tolist()
            s_values = hsv_image_clahe[..., 1][component_mask != 0].tolist()
            v_values = hsv_image_clahe[..., 2][component_mask != 0].tolist()
            
            # Calcular medianas
            mean_h = float(np.median(h_values)) if h_values else 0.0
            mean_s = float(np.median(s_values)) if s_values else 0.0
            mean_v = float(np.median(v_values)) if v_values else 0.0
            
            filename = f"{base_name}_cell_{label}"
            data = {
                "h_all": h_values,
                "s_all": s_values,
                "v_all": v_values,
                "mean_h": mean_h,
                "mean_s": mean_s,
                "mean_v": mean_v
            }
            
            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")


# Genera un archivo json de los valores HSV de cada célula anotada en una imagen en base a las máscara de los archivos NPY
# Se realiza normalizado z-score en el canal V
def obtener_datos_HSV_de_imagenes_normalizados(image_paths, mask_paths):
    if len(image_paths) != len(mask_paths):
        raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
    
    for image_path, mask_path in zip(image_paths, mask_paths):
        print(f"Analizando la imagen: {image_path}")

        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue
        
        try:
            mask = np.load(mask_path)
        except Exception as e:
            print(f"Error al cargar máscara {mask_path}: {e}")
            continue
        
        if image.shape[:2] != mask.shape:
            print(f"Error: Dimensiones no coinciden en {image_path}")
            continue
        
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Crear máscara para píxeles del fondo (no segmentados)
        background_mask = (mask == 0)

        # Extraer valores HSV del fondo
        h_global = hsv_image[..., 0][background_mask].ravel()
        s_global = hsv_image[..., 1][background_mask].ravel()
        v_global = hsv_image[..., 2][background_mask].ravel()

        # Calcular estadísticas globales (del fondo), manejar casos sin píxeles
        mean_h_global = float(np.mean(h_global)) if len(h_global) > 0 else 0.0
        std_h_global = float(np.std(h_global)) + 1e-8 if len(h_global) > 0 else 1.0

        mean_s_global = float(np.mean(s_global)) if len(s_global) > 0 else 0.0
        std_s_global = float(np.std(s_global)) + 1e-8 if len(s_global) > 0 else 1.0

        mean_v_global = float(np.mean(v_global)) if len(v_global) > 0 else 0.0
        std_v_global = float(np.std(v_global)) + 1e-8 if len(v_global) > 0 else 1.0

        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]

        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        

        carpeta_guardar_resultados = "HSV_normalizado"

        path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json


        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)
        save_data_paths = os.path.join(save_data_paths, base_name)

        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)

        # Procesar cada célula
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)

            # Valores HSV originales de la región
            h = hsv_image[..., 0][component_mask != 0]
            s = hsv_image[..., 1][component_mask != 0]
            v = hsv_image[..., 2][component_mask != 0]

            # Aplicar normalización Z-score usando estadísticas del fondo
            h_norm = ((h - mean_h_global) / std_h_global).tolist() if len(h) > 0 else []
            s_norm = ((s - mean_s_global) / std_s_global).tolist() if len(s) > 0 else []
            v_norm = ((v - mean_v_global) / std_v_global).tolist() if len(v) > 0 else []

            # Mediana de los valores normalizados
            mean_h_norm = float(np.median(h_norm)) if h_norm else 0.0
            mean_s_norm = float(np.median(s_norm)) if s_norm else 0.0
            mean_v_norm = float(np.median(v_norm)) if v_norm else 0.0

            filename = f"{base_name}_cell_{label}"

            # Guardar solo valores normalizados y estadísticas globales
            data = {
                "h_all": h_norm,
                "s_all": s_norm,
                "v_all": v_norm,
                "mean_h": mean_h_norm,
                "mean_s": mean_s_norm,
                "mean_v": mean_v_norm,

                # Estadísticas globales usadas para normalización (metadatos)
                "global_mean_h": mean_h_global,
                "global_std_h": std_h_global,
                "global_mean_s": mean_s_global,
                "global_std_s": std_s_global,
                "global_mean_v": mean_v_global,
                "global_std_v": std_v_global
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")



def obtener_datos_HSV_normalizados_de_imagenes_distancias(image_paths, mask_paths, threshold_zscore=3, threshold_min=15, 
                                                          threshold_max=60, threshold_max_area=0.7):
    try:
        if len(image_paths) != len(mask_paths):
            raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
        
        for image_path, mask_path in zip(image_paths, mask_paths):
            print("Analizando la imagen: ", image_path)

            image, mask, error = comprobar_imagenes_y_mascaras_correcta(image_path, mask_path)

            if error: # Si hay un error, continuar con la siguiente imagen
                continue
            
            # Conversión a RGB (OpenCV lee como BGR)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            distances, error = calcular_distancia_mahalanobis(rgb_image, image, mask)
            if error:
                print(f"Advertencia: No hay píxeles de fondo en {image_path}")
                continue

            
            # Normalización z-score global (usada para filtrado)
            mean_dist_global = np.mean(distances)
            std_dist_global = np.std(distances)
            zscore_global = (distances - mean_dist_global) / std_dist_global
            
            #print(f"Distancia de Mahalanobis calculada para {image_path}")
            #print(f"Media global de la distancia: {mean_dist_global}")
            #print(f"Desviación estándar global: {std_dist_global}")

            # Procesamiento de células
            labels_unicas = np.unique(mask)
            labels_unicas = labels_unicas[labels_unicas != 0]
            
            if len(labels_unicas) == 0:
                print(f"Advertencia: No hay células en {mask_path}")
                continue
            
            # Creación de directorios para resultados
            carpeta_guardar_resultados = "HSV"

            path_valores = create_path_new_folder(image_path, carpeta_guardar_resultados)
            base_name = os.path.splitext(os.path.basename(path_valores))[0]
            save_data_paths = os.path.dirname(path_valores)
            save_data_paths = os.path.join(save_data_paths, base_name)

            if not os.path.exists(save_data_paths):
                os.makedirs(save_data_paths, exist_ok=True)
            
            # Procesar cada célula
            for label in labels_unicas:
                component_mask = (mask == label).astype(np.uint8)
                
                # Extraer distancias y z-score global para los píxeles de la célula actual
                cell_distances = distances[component_mask != 0] # ya no lo uso
                cell_zscore = zscore_global[component_mask != 0]
                
                # Filtrar píxeles con z-score > threshold_zscore
                #thresholded_pixels = cell_zscore > threshold_zscore

                #thresholded_pixels = cell_distances > threshold_zscore

                thresholded_pixels = cell_zscore > threshold_zscore
                filtered_zscore = cell_zscore[thresholded_pixels]
                
                # Calcular estadísticas del z-score filtrado
                mean_zscore = float(np.mean(filtered_zscore)) if filtered_zscore.size > 0 else 0.0
                
                # Calcular área de tinción (porcentaje de píxeles filtrados)
                area_tincion = float(filtered_zscore.size) / float(cell_zscore.size) if cell_zscore.size > 0 else 0.0
                
                
                nivel_tincion  = "" # Provisional

                if ((len(filtered_zscore) == 0) or max(filtered_zscore) == 0.0): # Al poner lo del len al principio, me evito el 
                                                                                    # error de no porder hacer max de un array vacío
                    nivel_tincion = "sin tincion" 
                elif np.median(filtered_zscore) < np.percentile(zscore_global, threshold_min):
                    nivel_tincion = "minima"
                elif np.median(filtered_zscore) < np.percentile(zscore_global, threshold_max):
                    nivel_tincion = "media"
                elif np.median(filtered_zscore) >= np.percentile(zscore_global, threshold_max):
                    if area_tincion > threshold_max_area:
                        nivel_tincion = "maxima"
                    else:
                        nivel_tincion = "media"
                

            
                # Guardar datos en JSON
                filename = f"{base_name}_cell_{label}"
                data = {
                    "zscore_all": filtered_zscore.tolist(),          # Valores z-score filtrados
                    "mean_zscore": mean_zscore,                      # Promedio del z-score filtrado
                    "area_tincion": area_tincion,                    # Porcentaje de píxeles tintados
                    "nivel_tincion": nivel_tincion                   # Nivel de saturación en píxeles tintados
                }
                json_path = os.path.join(save_data_paths, f"{filename}.json")
                with open(json_path, "w") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"\n--- Resultados para {image_path} ---")
            print(f"Células analizadas: {len(labels_unicas)}")
            
        return crear_dir_resultados(carpeta_guardar_resultados) # devuelve el directorio donde se guardan los resultados
    except Exception as e:
        print(f" Error en obtener_datos_HSV: {e}")
        return ""



# Genera un archivo json de los valores RGB de cada célula anotada en una imagen en base a las máscara de los archivos NPY y
# devuelve el directorio global donde se guardan los resultados
# De los valores RGB se calculan las distancias de Mahalanobis y se aplica normalizado de z-score
def obtener_datos_RGB_normalizados_de_imagenes_distancias(image_paths, mask_paths, threshold_no_tincion=3, threshold_min=15, 
                                                          threshold_max=60, threshold_max_area=0.7):
    try:
        if len(image_paths) != len(mask_paths):
            raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
        
        for image_path, mask_path in zip(image_paths, mask_paths):
            print("Analizando la imagen: ", image_path)

            image, mask, error = comprobar_imagenes_y_mascaras_correcta(image_path, mask_path)

            if error: # Si hay un error, continuar con la siguiente imagen
                continue
            
            # Conversión a RGB (OpenCV lee como BGR)
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            distances, error = calcular_distancia_mahalanobis(rgb_image, image, mask)
            if error:
                print(f"Advertencia: No hay píxeles de fondo en {image_path}")
                continue

            # Obtención de las células
            labels_unicas = np.unique(mask)
            labels_unicas = labels_unicas[labels_unicas != 0]
            
            if len(labels_unicas) == 0:
                print(f"Advertencia: No hay células en {mask_path}")
                continue
            
            media = np.mean(distances)
            desv_estandar = np.std(distances)

            # Creación de directorios para resultados
            carpeta_guardar_resultados = "RGB"

            base_name, save_data_paths = crear_dir_y_subdir_resultados(image_path, carpeta_guardar_resultados)

            # Procesar cada célula
            for label in labels_unicas:
                component_mask = (mask == label).astype(np.uint8)
                
                cell_distances = distances[component_mask != 0].tolist()

                cell_zscore = (cell_distances - media) / desv_estandar

                filtered_zscore = filtrado_zscore(cell_zscore, threshold_no_tincion) # Según me pone Raquel en GitHub no tengo que hacerlo
                
                # Calcular estadísticas del z-score filtrado
                #mean_zscore = float(np.mean(filtered_zscore)) if filtered_zscore.size > 0 else 0.0
                mean_zscore = float(np.mean(cell_zscore)) if cell_zscore.size > 0 else 0.0
                
                # Calcular área de tinción (porcentaje de píxeles filtrados)
                area_tincion = float(filtered_zscore.size) / float(cell_zscore.size) if cell_zscore.size > 0 else 0.0
                
                # Determinar nivel de tinción
                nivel_tincion = "" 
                
                nivel_tincion = clasificar_tincion(cell_zscore, area_tincion, threshold_no_tincion, threshold_min, threshold_max, threshold_max_area)

                # Guardar datos en JSON
                filename = f"{base_name}_cell_{label}"
                data = {
                    "zscore_all": cell_zscore.tolist(),          #filtered_zscore.tolist(),
                    "mean_zscore": mean_zscore,
                    "max_zscore": max(cell_zscore),                     
                    "area_tincion": area_tincion,                    
                    "nivel_tincion": nivel_tincion                   
                }
                json_path = os.path.join(save_data_paths, f"{filename}.json")
                with open(json_path, "w") as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"\n--- Resultados para {image_path} ---")
            print(f"Células analizadas: {len(labels_unicas)}")
            #exit()
            
        return crear_dir_resultados(carpeta_guardar_resultados)
    except Exception as e:
        print(f" Error en obtener_datos_RGB: {e}")
        return ""


""" 
dir_imagenes_y_mascaras_hsv =  ["../../Imagenes_entrenamiento_reescalado", "../../Imagenes_validacion_reescalado/"]

imagenes_hsv = []
mascaras_hsv = []

for directorio in dir_imagenes_y_mascaras_hsv:
    imagenes_hsv.extend(obter_lista_ficheiros(directorio, ".jpg"))
    mascaras_hsv.extend(obter_lista_ficheiros(directorio, ".npy"))
"""

#obtener_datos_LAB_de_imagenes(imagenes_hsv, mascaras_hsv)

#obtener_datos_HSV_de_imagenes_normalizacion_nueva(imagenes_hsv, mascaras_hsv, threshold_zscore=3)

#dir = obtener_datos_HSV_normalizados_de_imagenes_distancias(imagenes_hsv, mascaras_hsv, threshold_zscore=3)

#obtener_datos_RGB_normalizados_de_imagenes(imagenes_hsv, mascaras_hsv, threshold_zscore=3)

#obtener_datos_RGB_normalizados_de_imagenes_distancias(imagenes_hsv, mascaras_hsv, threshold_no_tincion=3, 
#                                                      threshold_min=10, threshold_max=20, threshold_max_area=0.7) 
