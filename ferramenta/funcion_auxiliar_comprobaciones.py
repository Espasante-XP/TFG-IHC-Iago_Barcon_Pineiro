
import json
from pathlib import Path
from utils import es_numero, es_nombre_archivo_valido


def obtener_parametros_configuracion_herramienta():
    """
    Carga los parámetros de configuración de la herramienta desde un archivo JSON y realiza comprobaciones de validez.
    Devuelve los parámetros necesarios para la segmentación de imágenes como un diccionario.
    """

    # Ruta al archivo JSON con los parámetros de la herramienta
    archivo_json = '../config/reconocimiento_y_clasificacion.json'

    nombre_archivo_salida_sin_extension = 'nombre_archivo_salida_sin_extension'
    nombre_dir_modelo_segmentacion = 'path_modelo_segmentacion'
    nombre_channels = 'channels'
    nombre_diameter = 'diameter'
    nombre_min_size = 'min_size'
    nombre_normalize = 'normalize'
    nombre_niter = 'niter'
    nombre_tile_overlap = 'tile_overlap'
    nombre_flow_threshold = 'flow_threshold'
    nombre_cellprob_threshold = 'cellprob_threshold'
    nombre_dir_modelo_clasificacion = 'path_modelo_clasificacion'


    archivo_abierto = open(archivo_json)

    valores_parametros_modelo = json.load(archivo_abierto)

    # Comprobaciones de que los valores cargados son correctos
    texto_valor_nombre_archivo_salida_sin_extension = valores_parametros_modelo[nombre_archivo_salida_sin_extension]

    if isinstance(texto_valor_nombre_archivo_salida_sin_extension, str) and es_nombre_archivo_valido(texto_valor_nombre_archivo_salida_sin_extension):
        if texto_valor_nombre_archivo_salida_sin_extension == "None":
            archivo_salida_sin_extension = None
        else:
            archivo_salida_sin_extension = texto_valor_nombre_archivo_salida_sin_extension
    else:
        print("Error, el valor introducido para el nombre del archivo de salida sin extensión no es válido")
        exit()

    texto_valor_dir_modelo = valores_parametros_modelo[nombre_dir_modelo_segmentacion]

    if ((texto_valor_dir_modelo.isalpha() and texto_valor_dir_modelo == "None") or (texto_valor_dir_modelo == "")):
        segmentation_file_path = None
        print("Warning: No se ha especificado un modelo, se empleará el modelo por defecto de Cellpose")
    elif(Path(texto_valor_dir_modelo).exists()): 
        segmentation_file_path = texto_valor_dir_modelo 
    else:
        print("Error, el valor introducido para el path al modelo no es válido")
        exit()

    
    texto_valor_dir_modelo_clasificacion = valores_parametros_modelo[nombre_dir_modelo_clasificacion]

    if(Path(texto_valor_dir_modelo_clasificacion).exists()): 
        clasification_file_path = texto_valor_dir_modelo_clasificacion 
    else:
        print("Error, el valor introducido para el path al modelo de clasificación no es válido")
        exit()


    valor_channels = valores_parametros_modelo[nombre_channels]

    # channels debe ser si o si una lista de dos elementos, cada uno de ellos un número entre 0 y 3
    if isinstance(valor_channels, list): 
        if not (len(valor_channels) == 2 and 
                all(isinstance(x, (int, float)) and 0 <= x <= 3 for x in valor_channels)):
            print(f"Error, el valor introducido para la variable {nombre_channels} no es válido")
            exit()
        # Si pasa todas las validaciones, asignar el valor
        channels = valor_channels
    else:
        print(f"Error, el valor introducido para la variable {nombre_channels} no es una lista")
        exit()


    texto_valor_diameter = valores_parametros_modelo[nombre_diameter]

    if(texto_valor_diameter.isdigit()):
        if(int(texto_valor_diameter) >= 0):
            valor_diameter = int(texto_valor_diameter)
        else:
            print("Error, el valor introducido para la variable diameter no es válido")
            exit()
    elif ((texto_valor_diameter.isalpha() and texto_valor_diameter == "None") or (texto_valor_diameter == "")):
        valor_diameter = None
        print("Warning: No se ha especificado un valor para el diámetro, el modelo estimará el valor")
    else:
        print("Error, el valor introducido para la variable diameter no es válido")
        exit()
        

    texto_valor_min_size = valores_parametros_modelo[nombre_min_size]

    if(texto_valor_min_size.isdigit()):
        if(int(texto_valor_min_size) >= 0):
            valor_min_size = int(texto_valor_min_size)
        else:
            print("Error, el valor introducido para la variable min_size no es válido")
            exit()
        if(((valor_min_size > valor_diameter) and (valor_diameter is not None)) or ((valor_min_size >= 0) and (valor_diameter is None))):
            print("Warning: el valor de la variable min_size es mayor que el valor de la variable diameter")
    elif ((texto_valor_min_size.isalpha() and texto_valor_min_size == "None") or (texto_valor_min_size == "")):
        valor_min_size = None
    else:
        print("Error, el valor introducido para la variable min_size no es válido")
        exit()


    texto_valor_normalize = valores_parametros_modelo[nombre_normalize]

    if(texto_valor_normalize.isalpha() and texto_valor_normalize == "True"):
        valor_normalize = True
    elif (texto_valor_normalize.isalpha() and texto_valor_normalize == "False"):
        valor_normalize = False
    else:
        print("Error, el valor introducido para la variable normalize no es válido")
        exit()


    texto_valor_niter = valores_parametros_modelo[nombre_niter]

    if(texto_valor_niter.isdigit()):
        valor_niter = int(texto_valor_niter)
    elif (texto_valor_niter.isalpha() and texto_valor_niter == "None"):
        valor_niter = None
    else:
        print("Error, el valor introducido para la variable niter no es válido")
        exit()


    texto_valor_tile_overlap = valores_parametros_modelo[nombre_tile_overlap]

    if(es_numero(texto_valor_tile_overlap)):
        valor_tile_overlap = float(texto_valor_tile_overlap)
    elif (texto_valor_tile_overlap.isalpha() and texto_valor_tile_overlap == "None"):
        valor_tile_overlap = None
    else:
        print("Error, el valor introducido para la variable tile_overlap no es válido")
        exit()


    texto_valor_flow_threshold = valores_parametros_modelo[nombre_flow_threshold]

    if(es_numero(texto_valor_flow_threshold)):
        valor_flow_threshold = float(texto_valor_flow_threshold)
    elif (texto_valor_flow_threshold.isalpha() and texto_valor_flow_threshold == "None"):
        valor_flow_threshold = None
    else:
        print("Error, el valor introducido para la variable flow_threshold no es válido")
        exit()


    texto_valor_cellprob_threshold = valores_parametros_modelo[nombre_cellprob_threshold]

    if(es_numero(texto_valor_cellprob_threshold)):
        valor_cellprob_threshold = float(texto_valor_cellprob_threshold)
    elif (texto_valor_cellprob_threshold.isalpha() and texto_valor_cellprob_threshold == "None"):
        valor_cellprob_threshold = None
    else:
        print("Error, el valor introducido para la variable cellprob_threshold no es válido")
        exit()


    diccionario_parametros = {
        nombre_archivo_salida_sin_extension: archivo_salida_sin_extension,
        nombre_dir_modelo_segmentacion: segmentation_file_path,
        nombre_channels: channels,
        nombre_diameter: valor_diameter,
        nombre_min_size: valor_min_size,
        nombre_normalize: valor_normalize,
        nombre_niter: valor_niter,
        nombre_tile_overlap: valor_tile_overlap,
        nombre_flow_threshold: valor_flow_threshold,
        nombre_cellprob_threshold: valor_cellprob_threshold,
        nombre_dir_modelo_clasificacion: clasification_file_path
    }

    return diccionario_parametros
