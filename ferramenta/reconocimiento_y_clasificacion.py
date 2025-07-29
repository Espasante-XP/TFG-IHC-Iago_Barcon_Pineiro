
import os
from cellpose import models as modelsCellpose
from cellpose import io
from utils import obter_lista_ficheiros, get_final_folder_name
from funcion_auxiliar_comprobaciones import obtener_parametros_configuracion_herramienta
from clasificacion_empleando_red_neuronal import classify_staining
import cv2
import argparse
import gc
from pathlib import Path


csv_inicializado = False  # Variable para controlar si el CSV se ha inicializado


def contar_celulas_por_tincion_y_crear_CSV(nombre_imagen, tinciones_predichas, nombre_archivo_csv="imagenes_procesadas", 
                                           directorio_salida=None):
    """
    Cuenta el número de células por tinción y crea un archivo CSV con los resultados.
        :param nombre_imagen (str): Nombre de la imagen procesada.
        :param tinciones_predichas (list): Lista de tinciones predichas para cada célula.
        :return: None
    """

    global csv_inicializado  # Variable global para controlar si el CSV ha sido inicializado

    # Contar el número de células por tinción
    conteo_tinciones = {}
    lista_tinciones = [0,1,2,3]
    for tincion in lista_tinciones:
        conteo_tinciones[tincion] = 0

    for tincion in tinciones_predichas:
        if tincion not in conteo_tinciones:
            conteo_tinciones[tincion] = 0
        conteo_tinciones[tincion] += 1


    nombre_imagen = get_final_folder_name(nombre_imagen)  # Obtener el nombre de la imagen sin el path

    if directorio_salida is not None:
        archivo_csv_final = os.path.join(directorio_salida, nombre_archivo_csv + ".csv")  # Nombre del archivo CSV final
    else:
        directorio_salida = "./resultados_analisis"
        os.makedirs(directorio_salida, exist_ok=True)
        archivo_csv_final = os.path.join(directorio_salida, nombre_archivo_csv + ".csv")  # Nombre del archivo CSV final

    if csv_inicializado == False:
        with open(archivo_csv_final, "w") as csv_file:
            csv_file.write("Nombre Imagen,Numero Total Celulas,Sin tincion,Tincion Minima,Tincion Media,Tincion Maxima\n")
            csv_file.write(f"{nombre_imagen},{len(tinciones_predichas)}") 
            for tincion, conteo in conteo_tinciones.items():
                csv_file.write(f",{conteo}")
            csv_file.write(f"\n")
        csv_inicializado = True  # Marcar que el CSV ha sido inicializado
        print(f"Archivo CSV creado: {archivo_csv_final}")

    else:
        with open(archivo_csv_final, "a") as csv_file:
            csv_file.write(f"{nombre_imagen},{len(tinciones_predichas)}") 
            for tincion, conteo in conteo_tinciones.items():
                csv_file.write(f",{conteo}")
            csv_file.write(f"\n")

    
def segmentar_y_clasificar(imagen, diccionario_parametros_modelo, dir_salida=None):

    image = None

    segmentation_file_path = diccionario_parametros_modelo['path_modelo_segmentacion'] 
    channels = diccionario_parametros_modelo['channels']
    valor_diameter = diccionario_parametros_modelo['diameter']
    valor_min_size = diccionario_parametros_modelo['min_size']
    valor_normalize = diccionario_parametros_modelo['normalize']
    valor_niter = diccionario_parametros_modelo['niter']
    valor_tile_overlap = diccionario_parametros_modelo['tile_overlap']
    valor_flow_threshold = diccionario_parametros_modelo['flow_threshold']
    valor_cellprob_threshold = diccionario_parametros_modelo['cellprob_threshold']
    clasification_file_path = diccionario_parametros_modelo['path_modelo_clasificacion']

    modelo_cellpose = None

    image = io.imread(imagen)  # Leer la imagen usando la función propia de Cellpose
    
    try: 
        if segmentation_file_path is not None:
            modelo_cellpose = modelsCellpose.CellposeModel(gpu=True, pretrained_model=segmentation_file_path) 
        else:
            modelo_cellpose = modelsCellpose.Cellpose(gpu=True, model_type='cyto')
    except Exception as e:
        print(f"Error: {e}")
        print("No se ha podido cargar el modelo")
        exit()

    if(valor_min_size is None):
        resultado = modelo_cellpose.eval(image, diameter=valor_diameter, channels=channels, normalize=valor_normalize,
                flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
                niter=valor_niter, tile_overlap=valor_tile_overlap, progress=True)
    else:     
        resultado = modelo_cellpose.eval(image, diameter=valor_diameter, channels=channels, normalize=valor_normalize,
             flow_threshold=valor_flow_threshold, cellprob_threshold=valor_cellprob_threshold,
            min_size=valor_min_size, niter=valor_niter, tile_overlap=valor_tile_overlap, progress=True)

    if len(resultado) == 3: 
        masks, flows, styles = resultado 
    else: 
        masks, flows, styles, diams = resultado
    
    image = cv2.imread(imagen, cv2.COLOR_BGR2RGB) 

    tinciones_predichas = classify_staining(clasification_file_path, image, masks)

    nombre_archivo_salida = diccionario_parametros_modelo['nombre_archivo_salida_sin_extension']

    if nombre_archivo_salida is not None:
        contar_celulas_por_tincion_y_crear_CSV(imagen, tinciones_predichas, nombre_archivo_csv=nombre_archivo_salida, directorio_salida=dir_salida)
    else:
        contar_celulas_por_tincion_y_crear_CSV(imagen, tinciones_predichas, directorio_salida=dir_salida)



def main():

    parser = argparse.ArgumentParser(description='Procesar imaxes e xerar un arquivo co número de células por tinción')
    parser.add_argument('-d','--dir', type=str, required=True, help='Directorio con imaxes a procesar')
    parser.add_argument('--output_dir', type=str, default=None, help='Directorio de saída para os arquivos procesados (opcional)')
    args = parser.parse_args()

    directorio_imagenes = args.dir

    if not Path(directorio_imagenes).exists():
        print(f"Error: O directorio {directorio_imagenes} non existe.")
        return 1

    if not os.path.isdir(directorio_imagenes):
        print(f"Error: {directorio_imagenes} non é un directorio válido.")
        return 1

    lista_extensiones = ['.jpg', '.jpeg', '.png', '.tif', '.tiff']  # Extensiones de imagenes a buscar

    lista_imagenes = []

    for extension in lista_extensiones:
        lista_imagenes.extend(obter_lista_ficheiros(directorio_imagenes, extension))

    if not lista_imagenes:
        print(f"Non se atoparon imaxes no directorio especificado {directorio_imagenes}.")
        return 1


    dir_salida = args.output_dir

    # Crear el directorio de salida si no existe
    if dir_salida and not Path(dir_salida).exists():
        os.makedirs(dir_salida, exist_ok=True)



    diccionario_parametros_modelo = obtener_parametros_configuracion_herramienta()

    for imagen in lista_imagenes:
        print(f"Procesando imagen: {imagen}")

        segmentar_y_clasificar(imagen, diccionario_parametros_modelo, dir_salida)

        print(f"Imagen procesada: {imagen}")
        print()
        gc.collect()  # Limpiar la memoria después de procesar cada imagen


if __name__ == "__main__":
    main()
