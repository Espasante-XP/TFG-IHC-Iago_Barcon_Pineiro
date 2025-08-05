# TFG: Validación visual automática de biomarcadores mediante a técnica IHC en tecnoloxía farmacéutica 

Este repositorio contén os programas creados como parte do meu Traballo de Fin de Grao (TFG) sobre a creación dunha ferramenta para a detección e clasificación de células tratadas con IHC en base á tinción das mesmas.

## Índice
 - [Requisitos](#requisitos)
 - [Información relevante](#información-relevante)
   - [Recomendacións](#recomendacións-para-a-execución)
   - [Programas](#programas)
     - [Programas do directorio fonte](#programas-do-directorio-fonte)
     - [Programas do directorio da ferramenta](#programas-do-directorio-da-ferramenta)
   - [Ficheiros de configuración](#ficheiros-de-configuración)
 - [Uso](#uso)
   - [Creación do entorno](#creación-do-entorno)
   - [Uso da ferramenta](#uso-da-ferramenta)
 - [Contacto](#contacto)


## Requisitos
- **Entorno**: Python 3.8 ou superior empregando [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) e o ficheiro de entorno `environment.yml`.

- **Librarías**: 
  - `Cellpose` libraría principal do modelo de segmentación de imaxes empregado neste traballo.
  - `Pytorch` libraría principal do modelo de clasificación de imaxes empregado neste traballo.
  - `Pycocotools` libraría encargada de obter a información dos valores de referencia pertencentes ás anotacións gardadas en ficheiros JSON con formato COCO.
  - `Numpy` libraría obrigatoria para poder manexar os resultados do modelo de segmentación.
  - `OpenCV` libraría que contén todas as funcións empregadas no procesamento de imaxes.
  - `Scikit-learn` libraría da que se obteñen as función empregadas para avaliar o grao de precisión da clasificación de imaxes.
  - `cuda` libraría necesaria para que o entorno recoñeza a presenza da gráfica e permite aproveitar ao máxima as capacidades das GPUs de NVIDIA.

 - ***Cuda toolkit***: kit de ferramentas de CUDA, necesario para que o entorno recoñeza a gráfica e se poda usar na execución da ferramenta. A versión deste kit e a da libraría cuda do entorno deben coincidir. Neste caso empregouse a versión de cuda 12.6.

## Información relevante

### Recomendacións para a execución
Para o correcto funcionamento da ferramenta é aconsellable empregar unha computadora cunha tarxeta gráfica de NVIDIA, para que os modelos se poidan executar nela e así permitir que o porcesado de imaxes remate máis rápido.

En caso de querer empregar os modelos que se empregaron neste traballo é aconsellábel que a resolución das imaxes sexa de 648x486 píxeles ou resolucións similares. Esta resolución é a que se empregou no axuste do modelo cellpose e os valores dos parámetros axustados foron escollidos en relación con esta resolución. En caso de que as imaxes a analizar teñan unha resolución moi diferente á indicada anteriormente deberán modificarse os valores do ficheiro de configuración da ferramenta para que se axusten á nova resolución. O uso dunha resolución distinta da indicada pode afectar negativamente ao funcionamento da ferramenta.

O ficheiro CSV xerado reescribirá calquera ficheiro CSV co mesmo nome no directorio destino.

En caso de querer empregar o código do repositorio para adestrar un modelo de segmentación Cellpose distinto, hai que ter en conta que a función de avaliación do modelo de segmentación *boundary_scores* require unha gran cantidade de memoria durante a execución.

### Programas
Os programas do traballos divídense en dos directorios con diferentes propósitos, o directorio fonte (src) e o directorio da ferramenta (ferramenta).

#### Programas do directorio fonte

No directorio fonte están recollidos os programas empregados para o cálculo das métricas e os adestramentos e axustes dos modelos, así como outros programas auxiliares empregados para o manexo das anotacións en formato COCO. Dentro desde directorio existen dous subdirectorios, o directorio *cellpose* e o directorio *ihc*. Os programas máis relevantes son:

 - `train.py`: programa do subdirectorio *cellpose* que contén as funcións necesarias para adestramento do modelo de segmentación.
 - `reducir_tam_imagenes_y_mascaras.py`: programa do subdirectorio *ihc* empregado para reescalar as imaxes e as máscaras. O ficheiro de configuración é `preprocesado.json`.
 - `evaluar_segmentacion.py`: programa do subdirectorio *ihc* empregado para calcular as métricas do modelo de segmentación. O ficheiro de configuración é `modelo_cellpose.json`.
 - `entrenamiento.py`: programa do subdirectorio *ihc* que serve para adestrar o modelo de segmentación de Cellpose *cyto3*. O ficheiro de configuración é `entrenamiento_segmentacion.json`.
 - `clasificacion_empleando_red_neuronal.py`: programa do subdirectorio *ihc* empregado para axustar o modelo de clasificación e comprobar as métricas do mesmo. O ficheiro de configuración é `entrenamiento_clasificacion.json`
 - `crear_mascaras_de_anotaciones_coco.py`: programa do subdirectorio *ihc* que serve para crear as máscaras dun ficheiro de anotacións COCO. Existe outro ficheiro, chamado `crear_mascaras_coloridas_de_anotaciones_coco.py`, que xera as mesmas máscaras pero tinguidas para poder observar as distintas células anotadas. O ficheiro de configuración de ambos programas é `anotaciones_coco.json`.

#### Programas do directorio da ferramenta
No directorio da ferramenta están recollidos todos os programas necesarios para que se poda executar a ferramenta sen problemas. O ficheiro correspondente á ferramente é `reconocimiento_y_clasificacion.py`, que permite procesar todas as imaxes con extensión válida (png, jpg, jpeg, tif e tiff) dun directorio que se pasa como argumento. O ficheiro de configuración da ferramenta é `reconocimiento_y_clasificacion.json`. Este programa ten dous argumentos: 

  - -d ou --dir: argumento obrigatorio. Directorio a analizar que pode ser unha ruta absoluta ou relativa ao directorio onde se execute o comando.
  - --output_dir: argumento opcional. Directorio de saída onde se gardará o ficheiro resultando da execución do programa. Ten que introducirse un directorio válido podendo ser unha ruta absoluta ou relativa ao directorio onde se execute o comando.

### Ficheiros de configuración
Para poder poder facer un seguimento dos cambios que producen os distintos parámetros de configuración nas métricas creáronse os ficheiros de configuración, que se gardan no directorio *config* do directorio raíz. Os ficheiros de configuración existentes neste proxecto son:

| Nome do programa     | Descrición                               |
|------------------------|-------------------------------------------------------------------------------------------------------------------------|
| `anotaciones_coco.json` | Afecta aos programas `crear_mascaras_de_anotaciones_coco.py` e `crear_mascaras_coloridas_de_anotaciones_coco.py`. |
| `entrenamiento_clasificacion.json` | Afecta ao programa `clasificacion_empleando_red_neuronal.py`. |
| `entrenamiento_segmentacion.json` | Afecta ao programa `entrenamiento.py`. |
| `modelo_cellpose.json` | Afecta ao programa `evaluar_segmentacion.py`. |
| `preprocesado.json` | Afecta ao programa `reducir_tam_imagenes_y_mascaras.py`. |
| `reconocimiento_y_clasificacion.json` | Afecta ao programa `reconocimiento_y_clasificacion.py` |
| `umbrales_tincion.json` | Afecta ao programa `clasificar_umbrales_color.py`. |
 

As métricas froito das probas almacénanse no directorio *resultados*. 


## Uso

### Creación do entorno

 Para crear o entorno hai que situarse no directorio onde se almacene o ficheiro de entorno `environment.yml` e executar o comando:
```bash
    conda env create -f environment.yml
```
En caso de querer crear o entorno en Windows, debe empregarse o terminal que se descarga con miniconda.


### Uso da ferramenta

1. Clonar o repositorio:
    ```bash
    git clone https://github.com/Espasante-XP/TFG-IHC-Iago_Barcon_Pineiro.git
    ```
2. Moverse á carpeta onde se atopa o programa:
    ```bash
    cd TFG-IHC-Iago_Barcon_Pineiro/ferramenta
    ``` 
3. Executar o programa:
    ```bash
    python reconocimiento_y_clasificacion.py --dir dir_analizar
    ``` 


## Contacto

Para calquera dúbida ou suxerencia, por favor contacte conmigo a través de [iago.b.pineiro@gmail.com](mailto:iago.b.pineiro@gmail.com).

---

Este traballo é parte do meu TFG na [Universidade de Santiago de Compostela](https://www.usc.gal/gl), supervisado por [Xosé Manuel Pardo López](https://citius.gal/gl/team/xose-manuel-pardo-lopez/) como titor, e por [Raquel Dosil Lago](https://citius.gal/gl/team/raquel-dosil-lago/) e [Patricia Díaz Rodriguez](mailto:patricia.diaz.rodriguez@usc.es), como co-titoras.







