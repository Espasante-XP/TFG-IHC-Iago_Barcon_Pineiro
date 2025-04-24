
import cv2
import os
import numpy as np
from utils import obter_lista_ficheiros
import matplotlib.pyplot as plt
import json

dir_resultados = "../../valores_comp_conexas/HSV"

def create_metrics_name(directory_path):
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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


def create_metrics_name_rgb(directory_path):
    dir_resultados = "../../valores_comp_conexas/RGB"

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


def create_metrics_name_hsv(directory_path):

    dir_resultados = "../../valores_comp_conexas/HSV"

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


def create_metrics_name_lab(directory_path):
    dir_resultados = "../../valores_comp_conexas/LAB"

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


def create_metrics_name_clahe(directory_path):
    dir_resultados = "../../valores_comp_conexas/HSV_CLAHE"

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path


def create_metrics_name_hsv_normalizado(directory_path):
    dir_resultados = "../../valores_comp_conexas/HSV_normalizado"

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path
        


# Función para procesar imágenes con histogramas de color
def process_images_with_histograms(image_paths):
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if image is None:
            print(f"Error al leer: {image_path}")
            continue
        
        # Convertir a HSV y escala de grises
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        # Umbralización de Otsu
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        
        # Componentes conexas
        num_labels, labels, stats, _ = cv2.connectedComponentsWithStats(binary, 8, cv2.CV_32S)
        
        # Procesar cada componente (excluyendo el fondo)
        for i in range(1, num_labels):
            component_mask = (labels == i).astype("uint8") * 255
            
            # Extraer píxeles de la componente en HSV
            h = hsv_image[:, :, 0][component_mask != 0]
            s = hsv_image[:, :, 1][component_mask != 0]
            v = hsv_image[:, :, 2][component_mask != 0]
            
            # Calcular promedios
            mean_h, mean_s, mean_v = np.mean(h), np.mean(s), np.mean(v)
            
            # Crear histogramas
            plt.figure(figsize=(12, 4))
            
            # Histograma H (Tono)
            plt.subplot(1, 3, 1)
            plt.hist(h, bins=180, range=(0, 180), color='r', alpha=0.7)
            plt.title(f'Hue (Promedio: {mean_h:.1f})')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            
            # Histograma S (Saturación)
            plt.subplot(1, 3, 2)
            plt.hist(s, bins=256, range=(0, 255), color='g', alpha=0.7)
            plt.title(f'Saturation (Promedio: {mean_s:.1f})')
            plt.xlabel('Valor')
            
            # Histograma V (Brillo)
            plt.subplot(1, 3, 3)
            plt.hist(v, bins=256, range=(0, 255), color='b', alpha=0.7)
            plt.title(f'Value (Promedio: {mean_v:.1f})')
            plt.xlabel('Valor')
            
            plt.tight_layout()
            plt.show()
            
            # Mostrar información básica
            print(f"\nImagen: {image_path} | Componente: {i}")
            print(f"Área: {stats[i, cv2.CC_STAT_AREA]}")
            print(f"Bbox: X={stats[i, cv2.CC_STAT_LEFT]}, Y={stats[i, cv2.CC_STAT_TOP]}, "
                  f"W={stats[i, cv2.CC_STAT_WIDTH]}, H={stats[i, cv2.CC_STAT_HEIGHT]}")


# Funciona y genera un historgrama de las componentes conexas de cada célula anotada en una imagen en base a las máscara de los archivos NPY
def crear_histogramas_de_imagenes_y_mascaras_hsv(image_paths, mask_paths):
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
        

        path_valores = create_metrics_name_hsv(image_path)

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
            

            """ 
            # Crear histogramas
            plt.figure(figsize=(12, 4))
            
            # Histograma H
            plt.subplot(1, 3, 1)
            plt.hist(h, bins=180, range=(0, 180), color='r', alpha=0.7)
            plt.axvline(mean_h, color='black', linestyle='dashed', label=f'Prom: {mean_h:.1f}')
            plt.title('Tono (H)')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            plt.legend()
            
            # Histograma S
            plt.subplot(1, 3, 2)
            plt.hist(s, bins=256, range=(0, 255), color='g', alpha=0.7)
            plt.axvline(mean_s, color='black', linestyle='dashed', label=f'Prom: {mean_s:.1f}')
            plt.title('Saturación (S)')
            plt.xlabel('Valor')
            plt.legend()
            
            # Histograma V
            plt.subplot(1, 3, 3)
            plt.hist(v, bins=256, range=(0, 255), color='b', alpha=0.7)
            plt.axvline(mean_v, color='black', linestyle='dashed', label=f'Prom: {mean_v:.1f}')
            plt.title('Brillo (V)')
            plt.xlabel('Valor')
            plt.legend()
            
            # Configuración final de la figura
            plt.suptitle(f"Histogramas - {base_name} - Célula {label}", y=0.98)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            
            # Guardar gráfica y datos
            filename = f"{base_name}_cell_{label}"
            
            # Guardar PNG
            plt.savefig(os.path.join(save_data_paths, f"{filename}.png"))
            plt.close()
            """

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



def crear_histogramas_de_imagenes_y_mascaras_rgb(image_paths, mask_paths):
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
        

        path_valores = create_metrics_name_rgb(image_path)

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
            
            """ 
            # Crear histogramas
            plt.figure(figsize=(12, 4))
            
            # Histograma R
            plt.subplot(1, 3, 1)
            plt.hist(r, bins=256, range=(0, 255), color='r', alpha=0.7)
            plt.axvline(mean_r, color='black', linestyle='dashed', label=f'Prom: {mean_r:.1f}')
            plt.title('Rojo (R)')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            plt.legend()
            
            # Histograma G
            plt.subplot(1, 3, 2)
            plt.hist(g, bins=256, range=(0, 255), color='g', alpha=0.7)
            plt.axvline(mean_g, color='black', linestyle='dashed', label=f'Prom: {mean_g:.1f}')
            plt.title('Verde (G)')
            plt.xlabel('Valor')
            plt.legend()
            
            # Histograma B
            plt.subplot(1, 3, 3)
            plt.hist(b, bins=256, range=(0, 255), color='b', alpha=0.7)
            plt.axvline(mean_b, color='black', linestyle='dashed', label=f'Prom: {mean_b:.1f}')
            plt.title('Azul (B)')
            plt.xlabel('Valor')
            plt.legend()
            
            # Configuración final de la figura
            plt.suptitle(f"Histogramas - {base_name} - Célula {label}", y=0.98)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            
            # Guardar gráfica y datos
            filename = f"{base_name}_cell_{label}"
            
            # Guardar PNG
            plt.savefig(os.path.join(save_data_paths, f"{filename}.png"))
            plt.close()
            """

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


def crear_histogramas_de_imagenes_y_mascaras_lab(image_paths, mask_paths):
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

        path_valores = create_metrics_name_lab(image_path)

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

            # Crear histogramas
            plt.figure(figsize=(12, 4))

            # Histograma L
            plt.subplot(1, 3, 1)
            plt.hist(l, bins=256, range=(0, 255), color='gray', alpha=0.7)
            plt.axvline(mean_l, color='black', linestyle='dashed', label=f'Prom: {mean_l:.1f}')
            plt.title('Luminosidad (L)')
            plt.xlabel('Valor')
            plt.ylabel('Frecuencia')
            plt.legend()

            # Histograma A
            plt.subplot(1, 3, 2)
            plt.hist(a, bins=256, range=(0, 255), color='red', alpha=0.7)
            plt.axvline(mean_a, color='black', linestyle='dashed', label=f'Prom: {mean_a:.1f}')
            plt.title('Componente A')
            plt.xlabel('Valor')
            plt.legend()

            # Histograma B
            plt.subplot(1, 3, 3)
            plt.hist(b, bins=256, range=(0, 255), color='blue', alpha=0.7)
            plt.axvline(mean_b, color='black', linestyle='dashed', label=f'Prom: {mean_b:.1f}')
            plt.title('Componente B')
            plt.xlabel('Valor')
            plt.legend()

            # Configuración final de la figura
            plt.suptitle(f"Histogramas - {base_name} - Célula {label}", y=0.98)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])

            # Guardar gráfica y datos
            filename = f"{base_name}_cell_{label}"

            # Guardar PNG
            plt.savefig(os.path.join(save_data_paths, f"{filename}.png"))
            plt.close()

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

        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")

# Prueba para cambiar como se guardan los datos en el json (no me acabó de convencer)
def crear_histogramas_de_imagenes_y_mascaras_hsv_modif(image_paths, mask_paths):
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

        path_valores = create_metrics_name_hsv(image_path)
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
            
            # Calcular estadísticas
            stats = {}
            for channel, values in [('h', h), ('s', s), ('v', v)]:
                stats[f'mean_{channel}'] = float(np.mean(values)) if values else 0.0
                stats[f'median_{channel}'] = float(np.median(values)) if values else 0.0
                stats[f'max_{channel}'] = float(np.max(values)) if values else 0.0
            
            # Definir canales con sus identificadores EXPLÍCITOS
            channels = [
                ('Tono (H)', 'h', h, 0, 180, 'red'),
                ('Saturación (S)', 's', s, 0, 255, 'green'),
                ('Brillo (V)', 'v', v, 0, 255, 'blue')
            ]
            
            # Crear histogramas
            plt.figure(figsize=(15, 4))
            
            for i, (title, channel_code, data, min_val, max_val, color) in enumerate(channels, 1):
                plt.subplot(1, 3, i)
                plt.hist(data, bins=30, range=(min_val, max_val), color=color, alpha=0.7)
                
                # Usar channel_code para acceder a las estadísticas
                plt.axvline(stats[f'mean_{channel_code}'], color='black', 
                        linestyle='--', label=f'Media: {stats[f"mean_{channel_code}"]:.1f}')
                plt.axvline(stats[f'median_{channel_code}'], color='black',
                        linestyle='-.', label=f'Mediana: {stats[f"median_{channel_code}"]:.1f}')
                plt.axvline(stats[f'max_{channel_code}'], color='black',
                        linestyle=':', label=f'Máximo: {stats[f"max_{channel_code}"]:.1f}')
                
                plt.title(title)
                plt.xlabel('Valor')
                plt.ylabel('Frecuencia')
                plt.legend()
            
            # Configuración final de la figura
            plt.suptitle(f"Histogramas - {base_name} - Célula {label}", y=0.98)
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            
            # Guardar gráfica y datos
            filename = f"{base_name}_cell_{label}"
            
            # Guardar PNG
            plt.savefig(os.path.join(save_data_paths, f"{filename}.png"))
            plt.close()
            
            # Guardar JSON con todos los datos
            data_json = {
                "valores": {
                    "h": h,
                    "s": s,
                    "v": v
                },
                "estadisticas": {
                    "h": {
                        "media": stats['mean_h'],
                        "mediana": stats['median_h'],
                        "maximo": stats['max_h']
                    },
                    "s": {
                        "media": stats['mean_s'],
                        "mediana": stats['median_s'],
                        "maximo": stats['max_s']
                    },
                    "v": {
                        "media": stats['mean_v'],
                        "mediana": stats['median_v'],
                        "maximo": stats['max_v']
                    }
                }
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data_json, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")



def crear_histogramas_clahe_HSV(image_paths, mask_paths):
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
        
        path_valores = create_metrics_name_clahe(image_path)
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


# Falta cambiar el normalizado para que se haga a nivel de imagen en base a los valores del conjunto de la imagen y no de cada célula
def crear_histogramas_hsv_normalizado(image_paths, mask_paths):
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
        
        # Convertir a HSV y normalizar canales
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
        hsv_image[..., 0] /= 180.0  # H ∈ [0, 1]
        hsv_image[..., 1] /= 255.0  # S ∈ [0, 1]
        hsv_image[..., 2] /= 255.0  # V ∈ [0, 1]
        
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        
        path_valores = create_metrics_name_hsv_normalizado(image_path)
        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)
        save_data_paths = os.path.join(save_data_paths, base_name)
        
        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)
        
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            
            # Extraer valores HSV normalizados
            h = hsv_image[..., 0][component_mask != 0].tolist()
            s = hsv_image[..., 1][component_mask != 0].tolist()
            v = hsv_image[..., 2][component_mask != 0].tolist()
            
            # Calcular medianas (ya normalizadas)
            mean_h = float(np.median(h)) if h else 0.0
            mean_s = float(np.median(s)) if s else 0.0
            mean_v = float(np.median(v)) if v else 0.0
            
            filename = f"{base_name}_cell_{label}"
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


dir_imagenes_y_mascaras_hsv =  ["../../Imagenes_validacion_reescalado", "../../Imagenes_entrenamiento_reescalado"]

imagenes_hsv = []
mascaras_hsv = []

for directorio in dir_imagenes_y_mascaras_hsv:
    imagenes_hsv.extend(obter_lista_ficheiros(directorio, ".jpg"))
    mascaras_hsv.extend(obter_lista_ficheiros(directorio, ".npy"))


crear_histogramas_de_imagenes_y_mascaras_hsv(imagenes_hsv, mascaras_hsv)

crear_histogramas_de_imagenes_y_mascaras_rgb(imagenes_hsv, mascaras_hsv)

crear_histogramas_de_imagenes_y_mascaras_lab(imagenes_hsv, mascaras_hsv)

crear_histogramas_clahe_HSV(imagenes_hsv, mascaras_hsv)

crear_histogramas_hsv_normalizado(imagenes_hsv, mascaras_hsv)

