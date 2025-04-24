
import json, os
import matplotlib.pyplot as plt
import statistics, math
from collections import defaultdict
from statistics import median, mean


dir_guardado = "../../valores_clasif_tincion/resultados/"


# Obtiene una gráfica de los máximos de saturación dentro del umbral por imagen, pero
# cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_max_s_all_por_imagenes_arreglada(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    h_all = data.get('h_all', [])
                    s_all = data.get('s_all', [])
                    
                    if not (isinstance(h_all, list) and 
                            isinstance(s_all, list) and 
                            len(h_all) == len(s_all)):
                        continue
                    
                    # Filtrar valores en el umbral 90-130
                    s_filtrados = [s for h, s in zip(h_all, s_all) if 90 <= h <= 130] # Original 90 <= h <= 130

                    s_filtrados = s_all # <- Cambiado para usar s_all directamente
                    
                    # Obtener máximo por célula/archivo
                    if s_filtrados:
                        max_valor = max(s_filtrados)
                        datos_por_grupo[grupo_key][codigo_tincion].append(max_valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        # Preparar datos para las 4 variables de tinción
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)  # <- Calcula el máximo del conjunto
                
                # Etiqueta con el máximo en la leyenda
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',  # <- Muestra el máximo
                    edgecolor='w'
                )

        plt.title(f'Distribución s_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Valores máximos de s_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_max_s_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")



# Obtiene una gráfica del 10% de los valores superiores de saturación dentro del umbral por imagen, 
# cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_s_all_10_superior_por_imagenes(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    h_all = data.get('h_all', [])
                    s_all = data.get('s_all', [])
                    
                    if not (isinstance(h_all, list) and 
                            isinstance(s_all, list) and 
                            len(h_all) == len(s_all)):
                        continue
                    
                    # Filtrar valores en el umbral 90-130
                    s_filtrados = [s for h, s in zip(h_all, s_all) if 90 <= h <= 130] # Original 90 <= h <= 130

                    s_filtrados = s_all # <- Cambiado para usar s_all directamente
                    
                    if s_filtrados:
                        # Calcular el 10% superior
                        sorted_s = sorted(s_filtrados)
                        k = max(1, math.ceil(0.10 * len(sorted_s)))  # Mínimo 1 valor
                        top_10_percent = sorted_s[-k:]
                        
                        datos_por_grupo[grupo_key][codigo_tincion].extend(top_10_percent)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )

        plt.title(f'Distribución s_all (10% superior) - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Valores del 10% superior de s_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_10_superior_s_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


# Obtiene la media más la desviación estándar de los valores de saturación dentro del umbral por imagen,
# cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_s_all_media_mas_desv_estandar_por_imagenes(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    h_all = data.get('h_all', [])
                    s_all = data.get('s_all', [])
                    
                    if not (isinstance(h_all, list) and 
                            isinstance(s_all, list) and 
                            len(h_all) == len(s_all)):
                        continue
                    
                    # Filtrar valores en el umbral 90-130
                    s_filtrados = [s for h, s in zip(h_all, s_all) if 90 <= h <= 130] # Original 90 <= h <= 130

                    s_filtrados = s_all # <- Cambiado para usar s_all directamente
                    
                    if s_filtrados:
                        # Calcular media y desviación estándar
                        media = statistics.mean(s_filtrados)
                        desv_est = statistics.stdev(s_filtrados) if len(s_filtrados) >= 2 else 0.0
                        valor = media + desv_est
                        
                        datos_por_grupo[grupo_key][codigo_tincion].append(valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )

        plt.title(f'Distribución s_all (Media + DE) - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Media + Desviación Estándar de s_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_media_mas_de_s_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")




def RGB_grafica_distribucion_max_b_all_por_imagenes(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    b_all = data.get('b_all', [])
                    
                    if not (isinstance(b_all, list) and len(b_all) > 0):
                        continue
                    
                    # Obtener máximo por célula/archivo
                    max_valor = max(b_all)
                    datos_por_grupo[grupo_key][codigo_tincion].append(max_valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        # Preparar datos para las 4 variables de tinción
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)  # Máximo del conjunto
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )

        plt.title(f'Distribución b_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Valores máximos de b_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_max_b_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


def RGB_grafica_distribucion_b_all_10_superior_por_imagenes(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)  # Crear carpeta de salida [[4]]
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    b_all = data.get('b_all', [])
                    
                    if not isinstance(b_all, list) or len(b_all) == 0:
                        continue
                    
                    # Calcular el 10% superior sin filtrado previo
                    sorted_b = sorted(b_all)
                    k = max(1, math.ceil(0.10 * len(sorted_b)))  # Mínimo 1 valor
                    top_10_percent = sorted_b[-k:]
                    
                    datos_por_grupo[grupo_key][codigo_tincion].extend(top_10_percent)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos con nombres actualizados
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )

        plt.title(f'Distribución b_all (10% superior) - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Valores del 10% superior de b_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)  # Creación segura de directorios [[4]]
        
        nombre_archivo = f"grafica_distribucion_10_superior_b_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


def RGB_grafica_distribucion_b_all_media_mas_desv_estandar_por_imagenes(directorio_base, carpeta_salida):
    os.makedirs(carpeta_salida, exist_ok=True)
    
    carpetas = {
        'sin tincion': 0,
        'minima': 1,
        'media': 2,
        'maxima': 4
    }
    display_names = {
        0: 'Sin tinción',
        1: 'Mínima',
        2: 'Media',
        4: 'Máxima'
    }

    datos_por_grupo = defaultdict(lambda: defaultdict(list))

    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for root, _, files in os.walk(ruta_carpeta_tincion):
            rel_path = os.path.relpath(root, ruta_carpeta_tincion)
            depth = len(rel_path.split(os.sep)) if rel_path != '.' else 0
            
            if depth != 2:
                continue

            directorio_padre = os.path.basename(os.path.dirname(root))
            subdir2 = os.path.basename(root)
            grupo_key = (directorio_padre, subdir2)

            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    b_all = data.get('b_all', [])
                    
                    if not isinstance(b_all, list) or len(b_all) == 0:
                        continue
                    
                    # Calcular media + desviación estándar sin filtrado
                    media = statistics.mean(b_all)
                    desv_est = statistics.stdev(b_all) if len(b_all) >= 2 else 0.0
                    valor = media + desv_est
                    
                    datos_por_grupo[grupo_key][codigo_tincion].append(valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos con nombres actualizados
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        sin_tincion = datos.get(0, [])
        minima = datos.get(1, [])
        media = datos.get(2, [])
        maxima = datos.get(4, [])
        
        codigos = [0, 1, 2, 4]
        valores_por_codigo = [sin_tincion, minima, media, maxima]
        
        for codigo, valores in zip(codigos, valores_por_codigo):
            if valores:
                nombre_tipo = display_names[codigo]
                max_valor = max(valores)
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )

        plt.title(f'Distribución b_all (Media + DE) - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Media + Desviación Estándar de b_all')
        plt.xticks(codigos, [display_names[c] for c in codigos])
        plt.grid(True, alpha=0.3)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_media_mas_de_b_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


if __name__ == "__main__":
    
    directorio_archivos_clasif = "../../valores_clasif_tincion/normalizado_CLAHE/HSV" # "../../valores_clasif_tincion/normalizado/HSV"  "../../valores_clasif_tincion/auxiliar/HSV"

    directorio_salida = "../../valores_clasif_tincion/resultados/normalizado_CLAHE_graficas_distribucion/maximo_por_celula"
    directorio_salida_10_superior = "../../valores_clasif_tincion/resultados/normalizado_CLAHE_graficas_distribucion/10_superior"
    directorio_salida_media_y_dev_estandar = "../../valores_clasif_tincion/resultados/normalizado_CLAHE_graficas_distribucion/media_y_desv_estandar"



    grafica_distribucion_max_s_all_por_imagenes_arreglada(directorio_archivos_clasif, directorio_salida)
    grafica_distribucion_s_all_10_superior_por_imagenes(directorio_archivos_clasif, directorio_salida_10_superior)
    grafica_distribucion_s_all_media_mas_desv_estandar_por_imagenes(directorio_archivos_clasif, directorio_salida_media_y_dev_estandar)



    directorio_archivos_clasif_rgb = "../../valores_clasif_tincion/auxiliar/RGB" 

    directorio_salida_rgb = "../../valores_clasif_tincion/resultados/graficas_distribucion/RGB_maximo_por_celula"
    directorio_salida_10_superior_rgb = "../../valores_clasif_tincion/resultados/graficas_distribucion/RGB_10_superior"
    directorio_salida_media_y_dev_estandar_rgb = "../../valores_clasif_tincion/resultados/graficas_distribucion/RGB_media_y_desv_estandar"

    #RGB_grafica_distribucion_max_b_all_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_rgb)
    #RGB_grafica_distribucion_b_all_10_superior_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_10_superior_rgb)
    #RGB_grafica_distribucion_b_all_media_mas_desv_estandar_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_media_y_dev_estandar_rgb)

    exit()




