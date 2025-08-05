
import json, os
import matplotlib.pyplot as plt
import statistics, math
from collections import defaultdict
from statistics import mean
import numpy as np




# Obtiene una gráfica de los máximos de saturación dentro del umbral por imagen, pero
# cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_max_s_all_por_imagenes_arreglada(directorio_base, carpeta_salida, umbral_inferior=None, umbral_superior=None):
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
                    
                    if umbral_inferior is not None or umbral_superior is not None:
                        # Filtrar valores en el umbral 90-130
                        s_filtrados = [s for h, s in zip(h_all, s_all) if umbral_inferior <= h <= umbral_superior] # Original 90 <= h <= 130
                    else: 
                        # Si no se especifican umbrales, usar todos los valores
                        s_filtrados = s_all 
                    
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
# No es lo que se busca
def grafica_distribucion_s_all_10_superior_por_imagenes(directorio_base, carpeta_salida, umbral_inferior=None, umbral_superior=None):
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
                    
                    if umbral_inferior is not None or umbral_superior is not None:
                        # Filtrar valores en el umbral 90-130
                        s_filtrados = [s for h, s in zip(h_all, s_all) if umbral_inferior <= h <= umbral_superior] # Original 90 <= h <= 130
                    else: 
                        # Si no se especifican umbrales, usar todos los valores
                        s_filtrados = s_all 
                    
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



# Obtiene una gráfica de la media del 10% de los valores superiores de saturación dentro del 
# umbral por imagen, cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_s_all_mean_10_superior_por_imagenes(directorio_base, carpeta_salida, umbral_inferior=None, umbral_superior=None):
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
                    
                    if umbral_inferior is not None or umbral_superior is not None:
                        s_filtrados = [s for h, s in zip(h_all, s_all) if 
                                      (umbral_inferior <= h <= umbral_superior)]
                    else:
                        s_filtrados = s_all
                    
                    if s_filtrados:
                        sorted_s = sorted(s_filtrados)
                        k = max(1, math.ceil(0.10 * len(sorted_s)))
                        top_10_percent = sorted_s[-k:]
                        
                        mean_value = mean(top_10_percent)
                        
                        datos_por_grupo[grupo_key][codigo_tincion].append(mean_value)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        codigos = []
        valores_por_codigo = []
        
        for codigo in [0, 1, 2, 4]:
            valores = datos.get(codigo, [])
            if valores:
                codigos.append(codigo)
                valores_por_codigo.append(valores)
                max_valor = max(valores)
                nombre_tipo = display_names[codigo]
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.6,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w',
                    s=80
                )
        
        # Configuración del gráfico
        plt.title(f'Media del 10% superior de s_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Media del 10% superior de s_all')
        plt.xticks([0, 1, 2, 4], [display_names[c] for c in [0, 1, 2, 4]])
        plt.grid(True, alpha=0.3)
        
        # Mostrar leyenda
        if codigos:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Guardar gráfico
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_10_superior_s_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


# Obtiene la media más la desviación estándar de los valores de saturación dentro del umbral por imagen,
# cada grupo de valores se guarda por separado para evitar problemas
def grafica_distribucion_s_all_media_mas_desv_estandar_por_imagenes(directorio_base, carpeta_salida, umbral_inferior=None, umbral_superior=None):
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
                    
                    if umbral_inferior is not None or umbral_superior is not None:
                        # Filtrar valores en el umbral 90-130
                        s_filtrados = [s for h, s in zip(h_all, s_all) if umbral_inferior <= h <= umbral_superior] # Original 90 <= h <= 130
                    else: 
                        # Si no se especifican umbrales, usar todos los valores
                        s_filtrados = s_all 
                    
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


def grafica_distribucion_max_zscore_all_por_imagenes(directorio_base, carpeta_salida):
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
                    
                    # Solo usamos zscore_all y eliminamos el filtrado
                    zscore_all = data.get('zscore_all', [])
                    
                    # Validar que es una lista válida
                    if not isinstance(zscore_all, list):
                        continue
                    
                    # Obtener máximo directamente sin filtrado
                    if zscore_all:
                        max_valor = max(zscore_all)
                        datos_por_grupo[grupo_key][codigo_tincion].append(max_valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        codigos = []
        valores_por_codigo = []
        
        for codigo in [0, 1, 2, 4]:
            valores = datos.get(codigo, [])
            if valores:
                codigos.append(codigo)
                valores_por_codigo.append(valores)
                max_valor = max(valores)
                nombre_tipo = display_names[codigo]
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )
        
        # Configuración del gráfico actualizada
        plt.title(f'Distribución zscore_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Valores máximos de zscore_all')
        plt.xticks([0, 1, 2, 4], [display_names[c] for c in [0, 1, 2, 4]])
        plt.grid(True, alpha=0.3)
        
        # Mostrar leyenda
        if codigos:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Guardar gráfico
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_max_zscore_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_mean_10_superior_por_imagenes(directorio_base, carpeta_salida):
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
                    
                    # Solo usamos zscore_all y eliminamos todo filtrado por h_all
                    zscore_all = data.get('zscore_all', [])
                    
                    if not isinstance(zscore_all, list):
                        continue
                    
                    if zscore_all:
                        sorted_z = sorted(zscore_all)
                        k = max(1, math.ceil(0.10 * len(sorted_z)))
                        top_10_percent = sorted_z[-k:]
                        
                        mean_value = mean(top_10_percent)
                        datos_por_grupo[grupo_key][codigo_tincion].append(mean_value)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        codigos = []
        valores_por_codigo = []
        
        for codigo in [0, 1, 2, 4]:
            valores = datos.get(codigo, [])
            if valores:
                codigos.append(codigo)
                valores_por_codigo.append(valores)
                max_valor = max(valores)
                nombre_tipo = display_names[codigo]
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.6,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w',
                    s=80
                )
        
        # Configuración del gráfico actualizada
        plt.title(f'Media del 10% superior de zscore_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Media del 10% superior de zscore_all')
        plt.xticks([0, 1, 2, 4], [display_names[c] for c in [0, 1, 2, 4]])
        plt.grid(True, alpha=0.3)
        
        # Mostrar leyenda
        if codigos:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Guardar gráfico
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_10_superior_zscore_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_media_mas_desv_estandar_por_imagenes(directorio_base, carpeta_salida):
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
                    
                    # Solo usamos zscore_all y eliminamos el filtrado
                    zscore_all = data.get('zscore_all', [])
                    
                    if not isinstance(zscore_all, list):
                        continue
                    
                    if zscore_all:
                        # Calcular media y desviación estándar directamente
                        media = statistics.mean(zscore_all)
                        desv_est = statistics.stdev(zscore_all) if len(zscore_all) >= 2 else 0.0
                        valor = media + desv_est
                        
                        datos_por_grupo[grupo_key][codigo_tincion].append(valor)

                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráficos
    for (directorio_padre, subdir2), datos in datos_por_grupo.items():
        plt.figure(figsize=(10, 6))
        
        codigos = []
        valores_por_codigo = []
        
        for codigo in [0, 1, 2, 4]:
            valores = datos.get(codigo, [])
            if valores:
                codigos.append(codigo)
                valores_por_codigo.append(valores)
                max_valor = max(valores)
                nombre_tipo = display_names[codigo]
                
                plt.scatter(
                    [codigo] * len(valores),
                    valores,
                    alpha=0.5,
                    label=f'{nombre_tipo} (Máx: {max_valor:.2f})',
                    edgecolor='w'
                )
        
        # Configuración del gráfico actualizada
        plt.title(f'Media + DE de zscore_all - {directorio_padre}/{subdir2}')
        plt.xlabel('Código de intensidad')
        plt.ylabel('Media + Desviación Estándar de zscore_all')
        plt.xticks([0, 1, 2, 4], [display_names[c] for c in [0, 1, 2, 4]])
        plt.grid(True, alpha=0.3)
        
        # Mostrar leyenda
        if codigos:
            plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        # Guardar gráfico
        output_dir = os.path.join(carpeta_salida, directorio_padre)
        os.makedirs(output_dir, exist_ok=True)
        
        nombre_archivo = f"grafica_distribucion_media_mas_de_zscore_all_{subdir2}.png"
        ruta_salida = os.path.join(output_dir, nombre_archivo)
        plt.savefig(ruta_salida, bbox_inches='tight', dpi=300)
        plt.close()
        print(f"Gráfico guardado: {ruta_salida}")




def grafica_distribucion_max_zscore_all_1_grafica(directorio_base, carpeta_salida):
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

    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        # Iterar sobre cada carpeta de imágenes (ej: carpeta_imagenes3, IL6_3)
        for image_folder_entry in os.scandir(ruta_carpeta_tincion):
            if not image_folder_entry.is_dir():
                continue
            
            all_zscores = []
            
            # Recorrer todas las subcarpetas y archivos JSON dentro de la carpeta de imágenes
            for root, _, files in os.walk(image_folder_entry.path):
                for file in files:
                    if not file.lower().endswith('.json'):
                        continue
                    
                    archivo_path = os.path.join(root, file)
                    
                    try:
                        with open(archivo_path, 'r') as f:
                            data = json.load(f)
                        
                        zscore_all = data.get('zscore_all', [])
                        
                        if isinstance(zscore_all, list):
                            all_zscores.extend(zscore_all)
                            
                    except Exception as e:
                        print(f"Error en {archivo_path}: {str(e)}")
                        continue
            
            # Calcular el valor máximo por carpeta de imágenes
            if all_zscores:
                max_valor = max(all_zscores)
                datos_por_tincion[codigo_tincion].append(max_valor)

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        # Añadir jitter para evitar solapamiento
        x = np.random.normal(i, 0.05, size=len(valores)) # Hace que se vea más disperso
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Máx: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    # Configuración del gráfico
    plt.xticks(positions, labels)
    plt.title('Distribución de máximos zscore_all por carpeta de imágenes')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor máximo de zscore_all por carpeta')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    # Guardar gráfico
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_max_zscore_all_unica.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico único guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_mean_10_superior_1_grafica(directorio_base, carpeta_salida):
    """Calcula el máximo del 10% más grande de valores por carpeta"""
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

    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for image_folder_entry in os.scandir(ruta_carpeta_tincion):
            if not image_folder_entry.is_dir():
                continue
            
            all_zscores = []
            
            for root, _, files in os.walk(image_folder_entry.path):
                for file in files:
                    if not file.lower().endswith('.json'):
                        continue
                    
                    archivo_path = os.path.join(root, file)
                    
                    try:
                        with open(archivo_path, 'r') as f:
                            data = json.load(f)
                        
                        zscore_all = data.get('zscore_all', [])
                        
                        if isinstance(zscore_all, list):
                            all_zscores.extend(zscore_all)
                            
                    except Exception as e:
                        print(f"Error en {archivo_path}: {str(e)}")
                        continue
            
            if all_zscores:
                # Calcular top 10%
                sorted_vals = sorted(all_zscores, reverse=True)
                n = max(1, math.ceil(len(sorted_vals) * 0.1))
                top_vals = sorted_vals[:n]
                max_valor = max(top_vals) if top_vals else np.nan
                datos_por_tincion[codigo_tincion].append(max_valor)

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        x = np.random.normal(i, 0.05, size=len(valores))
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Max: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    plt.xticks(positions, labels)
    plt.title('Top 10% máximos zscore_all por carpeta')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor máximo del 10% superior')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_zscore_all_mean_10_superior.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico top10 guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_media_mas_desv_estandar_1_grafica(directorio_base, carpeta_salida):
    """Calcula media + desviación estándar de valores por carpeta"""
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

    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        for image_folder_entry in os.scandir(ruta_carpeta_tincion):
            if not image_folder_entry.is_dir():
                continue
            
            all_zscores = []
            
            for root, _, files in os.walk(image_folder_entry.path):
                for file in files:
                    if not file.lower().endswith('.json'):
                        continue
                    
                    archivo_path = os.path.join(root, file)
                    
                    try:
                        with open(archivo_path, 'r') as f:
                            data = json.load(f)
                        
                        zscore_all = data.get('zscore_all', [])
                        
                        if isinstance(zscore_all, list):
                            all_zscores.extend(zscore_all)
                            
                    except Exception as e:
                        print(f"Error en {archivo_path}: {str(e)}")
                        continue
            
            if all_zscores:
                # Calcular media + desviación estándar
                mean = np.mean(all_zscores)
                std = np.std(all_zscores)
                valor = mean + std
                datos_por_tincion[codigo_tincion].append(valor)

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        x = np.random.normal(i, 0.05, size=len(valores))
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Max: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    plt.xticks(positions, labels)
    plt.title('Media + Desviación Estándar de zscore_all por carpeta')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor (Media + σ)')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_zscore_all_media_mas_desv_estandar_1_grafica.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico media+std guardado: {ruta_salida}")




def grafica_distribucion_por_celula_max_zscore_all_1_grafica(directorio_base, carpeta_salida):
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

    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        # Recorrer todas las subcarpetas y archivos JSON
        for root, _, files in os.walk(ruta_carpeta_tincion):
            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    zscore_all = data.get('zscore_all', [])
                    
                    if isinstance(zscore_all, list) and zscore_all:
                        max_valor = max(zscore_all)
                        datos_por_tincion[codigo_tincion].append(max_valor)
                        
                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        # Añadir jitter para evitar solapamiento
        x = np.random.normal(i, 0.05, size=len(valores))
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Máx: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    # Configuración del gráfico
    plt.xticks(positions, labels)
    plt.title('Distribución de máximos zscore_all por archivo JSON')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor máximo de zscore_all por archivo')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    # Guardar gráfico
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_max_zscore_all_por_celula.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico único guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_por_celula_mean_10_superior_1_grafica(directorio_base, carpeta_salida):
    """Calcula el máximo del 10% más grande de valores por archivo JSON"""
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

    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        # Recorrer todos los archivos JSON en todos los subdirectorios
        for root, _, files in os.walk(ruta_carpeta_tincion):
            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    zscore_all = data.get('zscore_all', [])
                    
                    if isinstance(zscore_all, list) and zscore_all:
                        # Calcular top 10% para este archivo
                        sorted_vals = sorted(zscore_all, reverse=True)
                        n = max(1, math.ceil(len(sorted_vals) * 0.1))
                        top_vals = sorted_vals[:n]
                        
                        if top_vals:
                            max_valor = max(top_vals)
                            datos_por_tincion[codigo_tincion].append(max_valor)
                            
                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        # Añadir jitter para evitar solapamiento
        x = np.random.normal(i, 0.05, size=len(valores))
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Máx: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    # Configuración del gráfico actualizada
    plt.xticks(positions, labels)
    plt.title('Máximo del 10% superior de zscore_all por archivo')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor máximo del 10% superior por archivo')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    # Guardar gráfico
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_zscore_all_por_celula_mean_10_superior.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico único guardado: {ruta_salida}")


def grafica_distribucion_zscore_all_por_celula_media_mas_desv_estandar_1_grafica(directorio_base, carpeta_salida):
    """Calcula media + desviación estándar de zscore_all por archivo JSON"""
    try:
        # Asegurar que la carpeta de salida exista recursivamente
        os.makedirs(carpeta_salida, exist_ok=True)
        
        # Verificar que la carpeta realmente existe
        if not os.path.isdir(carpeta_salida):
            raise NotADirectoryError(f"La carpeta de salida no se pudo crear: {carpeta_salida}")

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

        datos_por_tincion = defaultdict(list)

        # Recolección de datos por tinción
        for nombre_carpeta, codigo_tincion in carpetas.items():
            ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
            
            if not os.path.exists(ruta_carpeta_tincion):
                print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
                continue

            # Recorrer todos los archivos JSON en todos los subdirectorios
            for root, _, files in os.walk(ruta_carpeta_tincion):
                for file in files:
                    if not file.lower().endswith('.json'):
                        continue
                    
                    archivo_path = os.path.join(root, file)
                    
                    try:
                        with open(archivo_path, 'r') as f:
                            data = json.load(f)
                        
                        zscore_all = data.get('zscore_all', [])
                        
                        if isinstance(zscore_all, list) and zscore_all:
                            # Calcular media + desviación estándar para este archivo
                            mean = np.mean(zscore_all)
                            std = np.std(zscore_all)  # Desviación estándar poblacional (ddof=0)
                            valor = mean + std
                            datos_por_tincion[codigo_tincion].append(valor)
                            
                    except Exception as e:
                        print(f"Error en {archivo_path}: {str(e)}")
                        continue

        # Generar gráfico único
        tincion_order = [0, 1, 2, 4]
        labels = [display_names[c] for c in tincion_order]
        positions = list(range(len(tincion_order)))

        plt.figure(figsize=(12, 7))
        
        for i, codigo in enumerate(tincion_order):
            valores = datos_por_tincion.get(codigo, [])
            
            if not valores:
                continue
            
            # Añadir jitter para evitar solapamiento
            x = np.random.normal(i, 0.05, size=len(valores))
            max_valor = max(valores)
            
            plt.scatter(
                x, 
                valores,
                alpha=0.6,
                label=f'{display_names[codigo]} (Máx: {max_valor:.2f})',
                edgecolor='w',
                s=60
            )
        
        # Configuración del gráfico actualizada
        plt.xticks(positions, labels)
        plt.title('Media + Desviación Estándar de zscore_all por archivo')
        plt.xlabel('Tipo de tinción')
        plt.ylabel('Valor (Media + σ)')
        plt.grid(True, axis='y', alpha=0.3)
        plt.legend(title='Intensidad de tinción')
        plt.tight_layout()
        
        # Guardar gráfico
        nombre_archivo = 'grafica_distribucion_zscore_all_por_celula_media_mas_desv_estandar_1_grafica.png'
        ruta_salida = os.path.join(carpeta_salida, nombre_archivo)

        print(f"Guardando gráfico en: {ruta_salida}")

        plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Gráfico único guardado: {ruta_salida}")
    
    except Exception as e:
        print(f"[ERROR] No se pudo guardar el gráfico: {str(e)}")


def grafica_distribucion_zscore_all_media_por_celula(directorio_base, carpeta_salida):
    """Genera una gráfica con los valores medios de zscore_all por archivo JSON"""
    os.makedirs(carpeta_salida, exist_ok=True)
    
    # Definiciones de categorías
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

    # Almacenamiento de datos
    datos_por_tincion = defaultdict(list)

    # Recolección de datos por tinción
    for nombre_carpeta, codigo_tincion in carpetas.items():
        ruta_carpeta_tincion = os.path.join(directorio_base, nombre_carpeta)
        
        if not os.path.exists(ruta_carpeta_tincion):
            print(f"[ERROR] Carpeta {nombre_carpeta} no existe")
            continue

        # Recorrer todos los archivos JSON en todos los subdirectorios
        for root, _, files in os.walk(ruta_carpeta_tincion):
            for file in files:
                if not file.lower().endswith('.json'):
                    continue
                
                archivo_path = os.path.join(root, file)
                
                try:
                    with open(archivo_path, 'r') as f:
                        data = json.load(f)
                    
                    zscore_all = data.get('zscore_all', [])
                    
                    if isinstance(zscore_all, list) and zscore_all:
                        # Calcular media para este archivo
                        media = np.mean(zscore_all)
                        datos_por_tincion[codigo_tincion].append(media)
                        
                except Exception as e:
                    print(f"Error en {archivo_path}: {str(e)}")
                    continue

    # Generar gráfico único
    tincion_order = [0, 1, 2, 4]
    labels = [display_names[c] for c in tincion_order]
    positions = list(range(len(tincion_order)))

    plt.figure(figsize=(12, 7))
    
    for i, codigo in enumerate(tincion_order):
        valores = datos_por_tincion.get(codigo, [])
        
        if not valores:
            continue
        
        # Añadir jitter para evitar solapamiento
        x = np.random.normal(i, 0.05, size=len(valores))
        max_valor = max(valores)
        
        plt.scatter(
            x, 
            valores,
            alpha=0.6,
            label=f'{display_names[codigo]} (Máx: {max_valor:.2f})',
            edgecolor='w',
            s=60
        )
    
    # Configuración del gráfico
    plt.xticks(positions, labels)
    plt.title('Media de zscore_all por archivo JSON')
    plt.xlabel('Tipo de tinción')
    plt.ylabel('Valor medio de zscore_all')
    plt.grid(True, axis='y', alpha=0.3)
    plt.legend(title='Intensidad de tinción')
    plt.tight_layout()
    
    # Guardar gráfico
    ruta_salida = os.path.join(carpeta_salida, 'grafica_distribucion_zscore_all_media_por_archivo.png')
    plt.savefig(ruta_salida, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Gráfico único guardado: {ruta_salida}")



# grafica_distribucion_zscore_all_por_celula_media_mas_desv_estandar_1_grafica

if __name__ == "__main__":
    
    directorio_datos = "../../valores_RGB_y_graficas_distancias/RGB" # MS BC RMB_1, FNB 3.12_3, FNB 4_3 y Control_negativo_2
    directorio_salida_base = "../../valores_RGB_y_graficas_distancias/graficas_distribucion_distancias_por_celula/"
    dir_salida_max = os.path.join(directorio_salida_base, "maximo_por_celula")
    dir_salida_10_superior = os.path.join(directorio_salida_base, "mean_10_superior")

    # No sé por que coño no funciona el directorio de salida si se crea sin problema
    dir_salida_media_y_dev_estandar = os.path.join(directorio_salida_base, "media_mas_desv_estandar")
    dir_salida_media_global = os.path.join(directorio_salida_base, "media_global")

    #dir_salida_media_y_dev_estandar = "../../valores_RGB_y_graficas_distancias/graficas_distribucion_distancias_por_celula/media_mas_desv_estandar"
    
    print("dir_salida_max:", dir_salida_max)
    print("dir_salida_10_superior:", dir_salida_10_superior)
    print("dir_salida_media_y_dev_estandar:", dir_salida_media_y_dev_estandar)
    #exit()

    
    grafica_distribucion_por_celula_max_zscore_all_1_grafica(directorio_datos, dir_salida_max)
    grafica_distribucion_zscore_all_por_celula_mean_10_superior_1_grafica(directorio_datos, dir_salida_10_superior)
    grafica_distribucion_zscore_all_por_celula_media_mas_desv_estandar_1_grafica(directorio_datos, dir_salida_10_superior)
    grafica_distribucion_zscore_all_media_por_celula(directorio_datos, dir_salida_media_global)

    exit()

    umbral_inferior = None
    umbral_superior = None

    directorio_archivos_clasif = "../../valores_clasif_tincion/HSV_normalizado" # "../../valores_clasif_tincion/normalizado/HSV"  "../../valores_clasif_tincion/auxiliar/HSV"

    directorio_salida = "../../valores_clasif_tincion/resultados/normalizado_graficas_distribucion/maximo_por_celula"
    directorio_salida_10_superior = "../../valores_clasif_tincion/resultados/normalizado_graficas_distribucion/mean_10_superior"
    directorio_salida_media_y_dev_estandar = "../../valores_clasif_tincion/resultados/normalizado_graficas_distribucion/media_y_desv_estandar"


    #grafica_distribucion_max_s_all_por_imagenes_arreglada(directorio_archivos_clasif, directorio_salida, umbral_inferior, umbral_superior)
    
    #grafica_distribucion_s_all_10_superior_por_imagenes(directorio_archivos_clasif, directorio_salida_10_superior, umbral_inferior, umbral_superior)
    
    #grafica_distribucion_s_all_mean_10_superior_por_imagenes(directorio_archivos_clasif, directorio_salida_10_superior, umbral_inferior, umbral_superior)
    #grafica_distribucion_s_all_media_mas_desv_estandar_por_imagenes(directorio_archivos_clasif, directorio_salida_media_y_dev_estandar, umbral_inferior, umbral_superior)


    directorio_archivos_clasif = "../../valores_clasif_tincion/RGB"

    directorio_salida_1_grafica = "../../valores_clasif_tincion/graficas_distribucion_distancias/maximo_1_grafica"
    directorio_salida_10_superior_1_grafica = "../../valores_clasif_tincion/graficas_distribucion_distancias/mean_10_superior_1_grafica"
    directorio_salida_media_y_dev_estandar_1_grafica = "../../valores_clasif_tincion/graficas_distribucion_distancias/media_y_desv_estandar_1_grafica"

    grafica_distribucion_max_zscore_all_1_grafica(directorio_archivos_clasif, directorio_salida_1_grafica)
    grafica_distribucion_zscore_all_mean_10_superior_1_grafica(directorio_archivos_clasif, directorio_salida_10_superior_1_grafica)
    grafica_distribucion_zscore_all_media_mas_desv_estandar_1_grafica(directorio_archivos_clasif, directorio_salida_media_y_dev_estandar_1_grafica)
    exit()


    directorio_archivos_clasif = "../../valores_clasif_tincion/HSV"
    directorio_salida = "../../valores_clasif_tincion/graficas_distribucion_distancias/maximo_por_celula"
    directorio_salida_10_superior = "../../valores_clasif_tincion/graficas_distribucion_distancias/mean_10_superior"
    directorio_salida_media_y_dev_estandar = "../../valores_clasif_tincion/graficas_distribucion_distancias/media_y_desv_estandar"

    grafica_distribucion_max_zscore_all_por_imagenes(directorio_archivos_clasif, directorio_salida)
    grafica_distribucion_zscore_all_mean_10_superior_por_imagenes(directorio_archivos_clasif, directorio_salida_10_superior)
    grafica_distribucion_zscore_all_media_mas_desv_estandar_por_imagenes(directorio_archivos_clasif, directorio_salida_media_y_dev_estandar)


    directorio_archivos_clasif_rgb = "../../valores_clasif_tincion/auxiliar/RGB" 

    directorio_salida_rgb = "../../valores_clasif_tincion/resultados_grafica_por_imagen/graficas_distribucion/RGB_maximo_por_celula"
    directorio_salida_10_superior_rgb = "../../valores_clasif_tincion/resultados_grafica_por_imagen/graficas_distribucion/RGB_10_superior"
    directorio_salida_media_y_dev_estandar_rgb = "../../valores_clasif_tincion/resultados_grafica_por_imagen/graficas_distribucion/RGB_media_y_desv_estandar"

    #RGB_grafica_distribucion_max_b_all_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_rgb)
    #RGB_grafica_distribucion_b_all_10_superior_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_10_superior_rgb)
    #RGB_grafica_distribucion_b_all_media_mas_desv_estandar_por_imagenes(directorio_archivos_clasif_rgb, directorio_salida_media_y_dev_estandar_rgb)

    print("Gráficas generadas y guardadas en las carpetas correspondientes.")

    exit()




