
import cv2
import os
import numpy as np
from utils import obter_lista_ficheiros
import matplotlib.pyplot as plt
import json

#dir_resultados_base = "../../valores_comp_conexas/"

dir_resultados_base = "../../parametros_HSV_RGB_LAB/"


def crear_dir_resultados(carpeta_guardar_resultados=None):
    return os.path.join(dir_resultados_base, carpeta_guardar_resultados)

def create_metrics_name(directory_path, carpeta_guardar_resultados):

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
    
    # Construir el nombre del archivo JSON
    full_name_metrics_archive = nombre_imagen_sin_extension + ".json"
    
    # Construir la ruta completa para el archivo JSON
    full_path = os.path.join(metrics_folder_path, full_name_metrics_archive)
    
    return full_path

def calcular_percentil(datos, percentil):
    """Calcula el percentil dado de una lista de valores."""
    # Convertir datos a una lista plana si es un array de NumPy
    if isinstance(datos, np.ndarray):
        datos = datos.flatten().tolist()
    if not datos:
        return 0.0  # Valor predeterminado para evitar errores   
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    if n == 0:
        return None
    k = (n - 1) * percentil / 100
    piso = int(k)
    techo = piso + 1
    fraccion = k - piso
    if techo >= n:
        return datos_ordenados[piso]
    return datos_ordenados[piso] * (1 - fraccion) + datos_ordenados[techo] * fraccion





# tengo que borrarlo, y borrar también la función donde se usa
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
        


# Funciona y genera un historgrama de las componentes conexas de cada célula anotada en una imagen en base a las máscara de los archivos NPY
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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json
    
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

            """ 
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
            """
            
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

        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")


# Prueba para cambiar como se guardan los datos en el json (no me acabó de convencer)
def obtener_datos_HSV_de_imagenes_modif(image_paths, mask_paths):
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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json

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
def obtener_datos_HSV_de_imagenes_normalizados_viejo(image_paths, mask_paths):
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

        # Calcular estadísticas globales (H, S, V) usando todos los píxeles
        h_global = hsv_image[:, :, 0].ravel()
        s_global = hsv_image[:, :, 1].ravel()
        v_global = hsv_image[:, :, 2].ravel()

        mean_h_global = np.mean(h_global)
        std_h_global = np.std(h_global) + 1e-8  # Evitar división por cero

        mean_s_global = np.mean(s_global)
        std_s_global = np.std(s_global) + 1e-8

        mean_v_global = np.mean(v_global)
        std_v_global = np.std(v_global) + 1e-8

        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]

        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue

        path_valores = create_metrics_name_hsv_normalizado(image_path) # Aquí se crea el path donde se guardará el json

        carpeta_guardar_resultados = "HSV_normalizado_viejo_mal"

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados)

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

            # Aplicar normalización Z-score
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
                "global_mean_h": float(mean_h_global),
                "global_std_h": float(std_h_global),
                "global_mean_s": float(mean_s_global),
                "global_std_s": float(std_s_global),
                "global_mean_v": float(mean_v_global),
                "global_std_v": float(std_v_global)
            }

            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w", encoding="utf-8") as f:  # Codificación explícita [[1]]
                json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")



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

        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados) # Aquí se crea el path donde se guardará el json


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



# En esta normalización se hace lo de la gaussiana del fondo, pero se hace un zscore de la distancia de Mahalanobis para cada pixel 
# y se umbraliza para obtener la máscara de tinción, luego se calcula el nivel de tinción como la mediana de los valores de 
# S de los píxeles que están en la máscara de tinción

# Está incompleto
# Se hacen todos los cálculos de distancias con los valores de RGB pero luego se devuelven los valores de HSV como si lo demás no importara
# No se realiza el cálculo de las distancias si no que se devuelven los valores normales de HSV
def obtener_datos_HSV_de_imagenes_normalizacion_nueva(image_paths, mask_paths, threshold_zscore=3):
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
        
        # Conversión a HSV y RGB
        hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # Para modelo gaussiano
        
        # Modelo gaussiano del fondo
        background_pixels = rgb_image[mask == 0].T  # Píxeles de fondo (label == 0)
        if background_pixels.size == 0:
            print(f"Advertencia: No hay píxeles de fondo en {image_path}")
            continue
        
        bg_mean = np.mean(background_pixels, axis=1)
        cov_matrix = np.cov(background_pixels)
        
        # Inversa de la matriz de covarianza (manejo de errores)
        try:
            inv_bg_cov = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            inv_bg_cov = np.linalg.pinv(cov_matrix)  # Pseudoinversa si es singular
        
        # Cálculo de la distancia de Mahalanobis para cada píxel
        distances = np.zeros(image.shape[:2])
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixel_rgb = rgb_image[i, j]
                diff = pixel_rgb - bg_mean
                dist = np.sqrt(np.dot(diff.T, np.dot(inv_bg_cov, diff)))
                distances[i, j] = dist
        
        print(f"Distancia de Mahalanobis calculada para {image_path}")
        print(f"Media de la distancia: {np.mean(distances)}")
        print(f"Desviación estándar de la distancia: {np.std(distances)}")


        # Normalización z-score y umbralización
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        zscore = (distances - mean_dist) / std_dist
        thresholded_mask = zscore > threshold_zscore  # Selección de píxeles tintados

        print(f"Valor de z-score: {zscore}")
        print("len(zscore): ", len(zscore))
        print(f"Umbralización aplicada con z-score: {threshold_zscore}")
        print(f"Porcentaje de píxeles tintados: {np.sum(thresholded_mask) / thresholded_mask.size * 100:.2f}%")
        exit()

        # Procesamiento de células
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        
        # Creación de directorios para resultados
        carpeta_guardar_resultados = "HSV"
        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados)

        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)
        save_data_paths = os.path.join(save_data_paths, base_name)

        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)
        
        # Procesar cada célula
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            cell_mask = (mask == label)
            
            # Extraer valores HSV (funcionalidad original)
            h = hsv_image[..., 0][cell_mask].tolist()
            s = hsv_image[..., 1][cell_mask].tolist()
            v = hsv_image[..., 2][cell_mask].tolist()
            
            # Calcular promedios HSV
            mean_h = float(np.median(h)) if h else 0.0
            mean_s = float(np.median(s)) if s else 0.0
            mean_v = float(np.median(v)) if v else 0.0
            
            # Cálculo de área y nivel de tinción
            stained_in_cell = np.logical_and(cell_mask, thresholded_mask)
            area_tincion = stained_in_cell.sum() / cell_mask.sum() if cell_mask.sum() > 0 else 0.0
            
            s_stained = hsv_image[..., 1][stained_in_cell].astype(float)
            nivel_tincion = float(np.median(s_stained)) if len(s_stained) > 0 else 0.0
            
            # Guardar datos en JSON
            filename = f"{base_name}_cell_{label}"
            data = {
                "h_all": h, 
                "s_all": s, 
                "v_all": v,
                "mean_h": mean_h, 
                "mean_s": mean_s, 
                "mean_v": mean_v,
                "area_tincion": area_tincion, 
                "nivel_tincion": nivel_tincion
            }
            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")



def obtener_datos_HSV_normalizados_de_imagenes_distancias(image_paths, mask_paths, threshold_zscore=3, threshold_min=0.15, 
                                                          threshold_max=0.6, threshold_max_area=0.5):
    try:
        if len(image_paths) != len(mask_paths):
            raise ValueError("La cantidad de imágenes y máscaras debe ser la misma")
        
        for image_path, mask_path in zip(image_paths, mask_paths):
            print("Analizando la imagen: ", image_path)

            # Leer la imagen y la máscara
            if not os.path.exists(image_path):
                print(f"Imagen no encontrada: {image_path}")
                continue

            if not os.path.exists(mask_path):
                print(f"Máscara no encontrada: {mask_path}")
                continue

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
            
            # Conversión a HSV
            hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
            # Modelo gaussiano del fondo (en HSV)
            background_pixels = hsv_image[mask == 0].T  # Píxeles de fondo (label == 0)
            if background_pixels.size == 0:
                print(f"Advertencia: No hay píxeles de fondo en {image_path}")
                continue
            
            bg_mean = np.mean(background_pixels, axis=1)
            cov_matrix = np.cov(background_pixels)
            
            # Inversa de la matriz de covarianza (manejo de errores)
            try:
                inv_bg_cov = np.linalg.inv(cov_matrix)
            except np.linalg.LinAlgError:
                inv_bg_cov = np.linalg.pinv(cov_matrix)  # Pseudoinversa si es singular
            
            # Cálculo de la distancia de Mahalanobis para cada píxel (en HSV)
            distances = np.zeros(image.shape[:2])
            for i in range(image.shape[0]):
                for j in range(image.shape[1]):
                    pixel_hsv = hsv_image[i, j]
                    diff = pixel_hsv - bg_mean
                    dist = np.sqrt(np.dot(diff.T, np.dot(inv_bg_cov, diff)))
                    distances[i, j] = dist
            
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

            path_valores = create_metrics_name(image_path, carpeta_guardar_resultados)
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
                median_zscore = float(np.median(filtered_zscore)) if filtered_zscore.size > 0 else 0.0
                
                # Calcular área de tinción (porcentaje de píxeles filtrados)
                area_tincion = float(filtered_zscore.size) / float(cell_zscore.size) if cell_zscore.size > 0 else 0.0
                
                # Calcular nivel de tinción (mediana del canal S en píxeles filtrados)
                s_values = hsv_image[..., 1][component_mask != 0][thresholded_pixels]

                #Para el nivel de tinción poner algo rollo, si sale 0.0, sin tinción, si en el 15% inferior, minima, si entre 15 y 60% 
                # media, si más que eso, maxima (valores sujetos a modificación)
                #nivel_tincion = float(np.median(s_values)) if s_values.size > 0 else 0.0
                
                nivel_tincion  = "" # Provisional

                """
                filename = f"{base_name}_cell_{label}"

                print("filename: ", filename)

                valor = calcular_percentil(zscore_global, threshold_max)

                print("np.median(filtered_zscore): ", np.median(filtered_zscore))

                print(f"Valor de percentil max: {valor}")

                print("type(zscore_global): ", type(zscore_global))

                valor = calcular_percentil(cell_zscore, 80)

                print(f"Valor de percentil max: {valor}")

                exit()

                """

                if ((len(filtered_zscore) == 0) or max(filtered_zscore) == 0.0): # Al poner lo del len al principio, me evito el 
                                                                                    # error de no porder hacer max de un array vacío
                    nivel_tincion = "sin tincion" #calcular_percentil
                elif np.median(filtered_zscore) < np.percentile(zscore_global, threshold_min): 
                    nivel_tincion = "minima" # zscore_global calcular_percentil
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
                    "median_zscore": median_zscore,                  # Mediana del z-score filtrado
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



def obtener_datos_RGB_normalizados_de_imagenes(image_paths, mask_paths, threshold_zscore=3):
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
        
        # Conversión a RGB
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Modelo gaussiano del fondo
        background_pixels = rgb_image[mask == 0].T  # Usar máscara para fondo [[anexo]]
        if background_pixels.size == 0:
            print(f"Advertencia: No hay píxeles de fondo en {image_path}")
            continue
        
        bg_mean = np.mean(background_pixels, axis=1)
        cov_matrix = np.cov(background_pixels)
        
        # Inversa de la matriz de covarianza (manejo de errores)
        try:
            inv_bg_cov = np.linalg.inv(cov_matrix)
        except np.linalg.LinAlgError:
            inv_bg_cov = np.linalg.pinv(cov_matrix)  # Pseudoinversa si es singular [[anexo]]
        
        # Cálculo de la distancia de Mahalanobis para cada píxel
        distances = np.zeros(image.shape[:2])
        for i in range(image.shape[0]):
            for j in range(image.shape[1]):
                pixel_rgb = rgb_image[i, j]
                diff = pixel_rgb - bg_mean
                dist = np.sqrt(np.dot(diff.T, np.dot(inv_bg_cov, diff)))
                distances[i, j] = dist
        
        # Normalización z-score [[anexo]]
        mean_dist = np.mean(distances)
        std_dist = np.std(distances)
        zscore = (distances - mean_dist) / std_dist

        
        print(f"Valor de z-score: {zscore}")
        print("len(zscore): ", len(zscore))
        #exit()
        
        # Procesamiento de células
        labels_unicas = np.unique(mask)
        labels_unicas = labels_unicas[labels_unicas != 0]
        
        if len(labels_unicas) == 0:
            print(f"Advertencia: No hay células en {mask_path}")
            continue
        
        # Creación de directorios para resultados
        carpeta_guardar_resultados = "RGB"  
        path_valores = create_metrics_name(image_path, carpeta_guardar_resultados)

        base_name = os.path.splitext(os.path.basename(path_valores))[0]
        save_data_paths = os.path.dirname(path_valores)
        save_data_paths = os.path.join(save_data_paths, base_name)
        if not os.path.exists(save_data_paths):
            os.makedirs(save_data_paths)
        
        # Procesar cada célula
        for label in labels_unicas:
            component_mask = (mask == label).astype(np.uint8)
            
            # Extraer valores z-score normalizados para esta célula
            zscore_cell = zscore[component_mask != 0].tolist()
            
            # Calcular promedio y mediana del z-score
            mean_zscore = float(np.mean(zscore_cell)) if zscore_cell else 0.0
            median_zscore = float(np.median(zscore_cell)) if zscore_cell else 0.0

            #print(f"Umbralización aplicada con z-score: {threshold_zscore}")
            #print(f"Porcentaje de píxeles tintados: {np.sum(thresholded_mask) / thresholded_mask.size * 100:.2f}%")
            
            # Guardar datos en JSON
            filename = f"{base_name}_cell_{label}"
            data = {
                "zscore_all": zscore_cell,
                "mean_zscore": mean_zscore,
                "median_zscore": median_zscore
            }
            json_path = os.path.join(save_data_paths, f"{filename}.json")
            with open(json_path, "w") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"\n--- Resultados para {image_path} ---")
        print(f"Células analizadas: {len(labels_unicas)}")
        exit()

"""
dir_imagenes_y_mascaras_hsv =  ["../../Imagenes_entrenamiento_reescalado", "../../Imagenes_validacion_reescalado/"]

imagenes_hsv = []
mascaras_hsv = []

for directorio in dir_imagenes_y_mascaras_hsv:
    imagenes_hsv.extend(obter_lista_ficheiros(directorio, ".jpg"))
    mascaras_hsv.extend(obter_lista_ficheiros(directorio, ".npy"))
"""

#obtener_datos_HSV_de_imagenes(imagenes_hsv, mascaras_hsv)

#obtener_datos_RGB_de_imagenes(imagenes_hsv, mascaras_hsv)

#obtener_datos_LAB_de_imagenes(imagenes_hsv, mascaras_hsv)

#obtener_datos_HSV_de_imagenes_clahe(imagenes_hsv, mascaras_hsv)

#obtener_datos_HSV_de_imagenes_normalizados(imagenes_hsv, mascaras_hsv)

#obtener_datos_HSV_de_imagenes_normalizacion_nueva(imagenes_hsv, mascaras_hsv, threshold_zscore=3)

#dir = obtener_datos_HSV_normalizados_de_imagenes_distancias(imagenes_hsv, mascaras_hsv, threshold_zscore=3)

#print("dir: ", dir)

#obtener_datos_RGB_normalizados_de_imagenes(imagenes_hsv, mascaras_hsv, threshold_zscore=3)
