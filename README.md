# TFG: Validación visual automática de biomarcadores mediante a técnica IHC en tecnoloxía farmacéutica 

Este repositorio contén os programas creados como parte do meu Traballo de Fin de Grao (TFG) sobre a creación dun programa para a detección e clasificación de células tratadas con IHC en base á tinción das mesmas.

## Requerimentos

- **Entorno**: Python 3.8 ou superior empregando miniconda e o arquivo de entorno `environment.yml`. Para crear o entorno:
        ```bash
        conda env create -f environment.yml
        ```

- **Librerías**: 
  - `Cellpose` que será empregada para o recoñecemento das células.
  - `Numpy` para o manejo das máscaras xeradas por cellpose.
  - `PIL` para o redimensionamento das imaxes (dito redimensionamento pode non ser necesario dependendo da memoria do dispositivo onde se execute)


## Uso

1. Clonar o repositorio:
    ```bash
    git clone https://github.com/Espasante-XP/TFG-IHC-Iago_Barcon_Pineiro.git
    ```
2. Moverse á carpeta onde se atopa o programa:
    ```bash
    cd python
    ``` 
3. Executar o programa:
    ```bash
    python run_cellpose.py
    ``` 
4. Axustar os parámetros para a creación das máscaras:
    Opcionalmente pódense modificar os parámetros de xeración de máscaras do arquivo Valores_para_evaluacion/parametros_model_eval.json


## Contacto

Para calquera dúbida ou suxerencia, por favor contacte conmigo a través de [iago.barcon@rai.usc.es](mailto:iago.barcon@rai.usc.es).

---

Este traballo é parte do meu TFG na [Universidade de Santiago de Compostela](https://www.usc.gal/gl), supervisado por [Xosé Manuel Pardo López](https://citius.gal/gl/team/xose-manuel-pardo-lopez/) como titor, e por [Raquel Dosil Lago](https://citius.gal/gl/team/raquel-dosil-lago/) e Patricia Díaz Rodriguez <patricia.diaz.rodriguez@usc.es> (non atopei o análogo), como co-titoras.







