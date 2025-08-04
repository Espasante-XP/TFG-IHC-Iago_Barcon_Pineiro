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
   - [Metricas](#métricas)
 - [Uso](#uso)
   - [Creación do entorno](#creación-do-entorno)
   - [Uso da ferramenta](#uso-da-ferramenta)
 - [Contacto](#contacto)


## Requisitos

Creo que esto lo puedo meter mejor en la sección de Requisitos e recomendacións

- **Entorno**: Python 3.8 ou superior empregando [miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) e o arquivo de entorno `environment.yml`.

- **Librarías**: 
  - `Cellpose` libraría principal do modelo de segmentación de imaxes empregado neste traballo.
  - `Pytorch` libraría principal do modelo de clasificación de imaxes empregado neste traballo.
  - `Pycocotools` libraría encargada de obter a información dos valores de referencia pertencentes ás anotacións gardadas en arquivos JSON con formato COCO.
  - `Numpy` libraría obrigatoria para poder manexar os resultados do modelo de segmentación.
  - `OpenCV` libraría que contén todas as funcións empregadas no procesamento de imaxes.
  - `Scikit-learn` libraría da que se obteñen as función empregadas para avaliar o grao de precisión da clasificación de imaxes.
  - `cuda` libraría necesaria para que o entorno recoñeza a presenza da gráfica e permite aproveitar ao máxima as capacidades das GPUs de NVIDIA.

 - ***Cuda toolkit***: kit de ferramentas de CUDA, necesario para que o entorno recoñeza a gráfica e se poda usar na execución da ferramenta. A versión deste kit e a da librería cuda do entorno deben coincidir. Neste caso empregouse a versión de cuda 12.6.

## Información relevante

### Recomendacións para a execución
Para o correcto funcionamento da ferramenta é aconsellable empregar unha computadora cunha tarxeta gráfica de NVIDIA, para que os modelos se poidan executar nela e así permitir que o porcesado de imaxes remate máis rápido.

En caso de querer empregar os modelos que se empregaron neste traballo é aconsellábel que a resolución das imaxes sexa de 648x486 píxeles ou resolucións similares. Esta resolución é a que se empregou no axuste do modelo cellpose e os valores dos parámetros axustados foron escollidos en relación con esta resolución. En caso de que as imaxes a analizar teñan unha resolución moi diferente á indicada anteriormente deberán modificarse os valores do arquivo de configuración da ferramenta para que se axusten á nova resolución. O uso dunha resolución distinta da indicada pode afectar negativamente ao funcionamento da ferramenta.

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
No directorio da ferramenta están recollidos todos os programas necesarios para que se poda executar a ferramenta sen problemas. O ficheiro correspondente á ferramente é `reconocimiento_y_clasificacion.py`, que permite procesar todas as imaxes con extensión válida (png, jpg, jpeg, tif e tiff) dun directorio que se pasa como argumento. O arquivo de configuración da ferramenta é `reconocimiento_y_clasificacion.json`. Este programa ten dous argumentos: 

  - -d ou --dir: argumento obrigatorio. Directorio a analizar que pode ser unha ruta absoluta ou relativa ao directorio onde se execute o comando.
  - --output_dir: argumento opcional. Directorio de saída onde se gardará o ficheiro resultando da execución do programa. Ten que introducirse un directorio válido podendo ser unha ruta absoluta ou relativa ao directorio onde se execute o comando.

### Ficheiros de configuración
Para poder poder facer un seguimento dos cambios que producen os distintos parámetros de configuración nas métricas creáronse os ficheiros de configuración. Estes ficheiros, pese a ser parte do programa, funcionan como elementos independentes ao mesmo, polo que se gardan no directorio *config* do directorio raíz. Os ficheiros de configuración existentes neste proxecto son:
 - `anotaciones_coco.json`: afecta aos programas `crear_mascaras_de_anotaciones_coco.py` e `crear_mascaras_coloridas_de_anotaciones_coco.py`. Os seus parámetros son: 
   - *path_imagenes*: ruta absoluta ou relativa onde se atopan as imaxes.
   - *path_anotaciones*: ruta absoluta ou relativa onde se atopan o ficheiro de anotacións en formato COCO.
   - *extension_imagen*: extensión da imaxe.
   - *sufijo_mascara*: sufixo que se engadirá ao arquivo resultante.

 - `entrenamiento_clasificacion.json`: afecta ao programa `clasificacion_empleando_red_neuronal.py`. Os seus parámetros son: 
   - *path_entrenamiento*: ruta absoluta ou relativa onde se atopan as imaxes e máscaras de adestramento.
   - *path_validacion*: ruta absoluta ou relativa onde se atopan as imaxes e máscaras de validación.
   - *path_anotaciones*: ruta absoluta ou relativa onde se atopan o ficheiros de anotacións en formato COCO.
   - *path_guardado_modelo*: ruta absoluta ou relativa onde se gardará o modelo.
   - *learning_rate*: ratio de aprendizaxe no adestramento.
   - *momentum*: ratio de aprendizaxe dunha época anterior
 do modelo con respecto á actual.
   - *step_size*: número de épocas tras as que se reducirá nunha proporción o ratio de aprendizaxe do modelo.
   - *gamma*:  proporción na que se reduce o ratio de aprendizaxe do modelo tras pasar step_size épocas.
   - *numero_epochs*: número de iteracións máximas que realizará o adestramento.
   - *batch_size*: número de imaxes a procesar simultáneamente.
   - *patience*:  número de épocas tras o que se parará o adestramento en caso de no haber mellora na media de perdas de validación.
   - *valor_perdidas_aceptable*: limiar que implica a parada inmediata do adestramento do modelo se aparece un valor menor a este nas perdas de adestramento.
   - *archivo_resultante*: nome do arquivo resultante.
   - *data_augmentation*: se aplica ou non a función de *data augmentation*.

 - `entrenamiento_segmentacion.json`: afecta ao programa `entrenamiento.py`. Os seus parámetros son: 
   - *path_entrenamiento*: ruta absoluta ou relativa onde se atopan as imaxes e máscaras de adestramento.
   - *path_validacion*: ruta absoluta ou relativa onde se atopan as imaxes e máscaras de validación.
   - *extension_imagen*: extensión das imaxes.
   - *extension_mascara*: extensión das máscaras.
   - *channels*: canles da imaxe ou imaxes. En caso de poñer máis dunha canle, o número de canles debe ser tantas como imaxes.
   - *normalize*: se aplica a normalización.
   - *weight_decay*: ratio de decaemento dos pesos.
   - *learning_rate*: ratio de aprendizaxe.
   - *batch_size*: número de imaxes a procesar simultáneamente.
   - *num_epochs*: número de iteracións máximas que realizará o adestramento.
   - *destino_reentrenamiento*: ruta absoluta ou relativa onde se gardará o modelo tras o destramento.
   - *guardar_cada*: cada cantas iteracións se garda o modelo.
   - *min_train_masks*: número mínimo de máscaras que debe ter unha imaxe para que se poda empregar para adestrar o modelo.

 - `modelo_cellpose.json`: afecta ao programa `evaluar_segmentacion.py`. Os seus parámetros son: 
   - *path_imagenes*: ruta absoluta ou relativa onde se atopan as imaxes.
   - *path_modelo*: ruta absoluta ou relativa do modelo de segmentación. 
   - *extension_imagen*:  extensión das imaxes.
   - *channels*: canles da imaxe ou imaxes. En caso de poñer máis dunha canle, o número de canles debe ser tantas como imaxes.
   - *diameter*: diámetro aproximado das células a analizar. En caso de non poñer ningún valor o modelo estimará un valor.
   - *min_size*: tamaño mínimo das células.
   - *normalize*:  se aplica a normalización.
   - *niter*: número de iteracións para a predición da segmentación.
   - *tile_overlap*: a superposición que pode haber entre os píxeles ao calcular os fluxos.
   - *flow_threshold*:  limiar por enriba do cal se descarta toda célula cuxa cantidade de erros supere ese valor.
   - *cellprob_threshold*: limiar por enriba do cal se aceptan todos os píxeles como máscaras. A medida que se reduce o valor por debaixo de 0 permite atopar máis máscaras e máscaras máis grandes.
   - *nombre_sufijo_mascara_pred*: sufixo para as máscaras preditas.
   - *sufijo_mascara_g_truth*: sufuxo das máscaras dos valores de referencia.

 - `preprocesado.json`: afecta ao programa `reducir_tam_imagenes_y_mascaras.py`. Os seus parámetros son: 
   - *escala*: escala á que se redimensionarán as imaxes e as máscaras. Con valor 1 a imaxe non se verá alterada.
   - *path_imagenes*: lista de directorios absolutos ou relativos de imaxes. Este directorio debe conter tamén as máscaras, as cales deben ter o mesmo nome que a imaxe.
   - *path_salida*: directorio absoluto ou relativo onde se gardarán as imaxes reescaladas.
   - *extension_imagen*: extensión das imaxes.
   - *extension_mascara*: extensión das máscaras.

 - `reconocimiento_y_clasificacion.json`: afecta ao programa `reconocimiento_y_clasificacion.py`. Os seus parámetros son: 
   - *nombre_archivo_salida_sin_extension*: nome do ficheiro que xera o programa tras porcesar as imaxes.
   - *path_modelo_segmentacion*: ruta absoluta ou relativa ao modelo de segmentación.
   - - *channels*: canles da imaxe ou imaxes. En caso de poñer máis dunha canle, o número de canles debe ser tantas como imaxes.
   - *diameter*: diámetro aproximado das células a analizar. En caso de non poñer ningún valor o modelo estimará un valor.
   - *min_size*: tamaño mínimo das células.
   - *normalize*:  se aplica a normalización.
   - *niter*: número de iteracións para a predición da segmentación.
   - *tile_overlap*: a superposición que pode haber entre os píxeles ao calcular os fluxos.
   - *flow_threshold*:  limiar por enriba do cal se descarta toda célula cuxa cantidade de erros supere ese valor.
   - *cellprob_threshold*: limiar por enriba do cal se aceptan todos os píxeles como máscaras. A medida que se reduce o valor por debaixo de 0 permite atopar máis máscaras e máscaras máis grandes.
   - *path_modelo_clasificacion*: ruta absoluta ou relativa ao modelo de clasificación.

 - `umbrales_tincion.json`: afecta ao programa `clasificar_umbrales_color.py`. Os seus parámetros son: 
   - *dir_imagenes_y_mascaras*: lista de directorios absolutos ou relativos de imaxes.
   - *dir_ground_truth_general*:  ruta absoluta ou relativa onde se atopan as imaxes e máscaras de adestramento.
   - *threshold_no_tincion*: limiar a partir do cal se considera que a célula ten tinción.
   - *threshold_min*: limiar a partir do cal se considera que a tinción da célula é media.
   - *threshold_max*: limiar a partir do cal se considera que a tinción da célula é máxima.
   - *threshold_max_area*: limiar de superficie tinguida que debe superar a célula para considerar que ten tinción máxima, en caso contrario a tinción será media.
   - *archivo_resultante*: nome do arquivo onde se gardarán as métricas resultado da clasificación.

### Métricas 
As métricas almacénanse no directorio *resultados*. Este directorio ten dous subdirectorios para almacenar as métricas correspondentes ás distintas probas realizadas: *clasificacion_tincion* e *segmentacion*. Nas probas de clasificación empréganse as métricas *precision*, *recall* *f1-score* e *accuracy* e a matriz de confusión; mentres que nas probas de segmentación calcúlase o índice de Jaccard, a *precision*, o *recall* e a *f1-score*.





## Uso

### Creación do entorno

 Para crear o entorno hai que situarse no directorio onde se alamcene o ficheiro de entorno `environment.yml` e exectutar o comando:
```bash
    conda env create -f environment.yml
```
En caso de querer crear o entorno en Windows debe empregarse o terminal que se descarga con miniconda.


### Uso da ferramenta

1. Clonar o repositorio:
    ```bash
    git clone https://github.com/Espasante-XP/TFG-IHC-Iago_Barcon_Pineiro.git
    ```
2. Moverse á carpeta onde se atopa o programa:
    ```bash
    cd ferramenta
    ``` 
3. Executar o programa:
    ```bash
    python reconocimiento_y_clasificacion.py --dir dir_analizar
    ``` 


## Contacto

Para calquera dúbida ou suxerencia, por favor contacte conmigo a través de [iago.b.pineiro@gmail.com](mailto:iago.b.pineiro@gmail.com).

---

Este traballo é parte do meu TFG na [Universidade de Santiago de Compostela](https://www.usc.gal/gl), supervisado por [Xosé Manuel Pardo López](https://citius.gal/gl/team/xose-manuel-pardo-lopez/) como titor, e por [Raquel Dosil Lago](https://citius.gal/gl/team/raquel-dosil-lago/) e [Patricia Díaz Rodriguez](mailto:patricia.diaz.rodriguez@usc.es), como co-titoras.







