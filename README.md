## Descripción
Este proyecto tiene como objetivo crear un sistema de recomendación de peliculas partiendo de una base de datos con informacion de estas.
Tambien se crean algunas funciones para poder consultar los datos desde una [API](https://proyecto-individual-1-henry-w5c2.onrender.com/docs#/)

## Tabla de contenido
1. [Instalación y Requisitos](#instalación-y-requisitos)
2. [Estructura del Proyecto](#estructura-del-proyecto)
3. [Uso y Ejecución](#uso-y-ejecución)
4. [Fuente de Datos](#fuente-de-datos)


## Instalación y Requisitos
**Requisitos:**
- Python 3.7 o superior
- pandas
- numpy
- matplotlib
- scikit-learn

**Pasos de instalación:**
1. Clonar el repositorio: `git clone https://github.com/thomasbraca/Sistema-de-Recomendacion-Peliculas/.git`
2. Crear un entorno virtual: `python -m venv venv`
3. Activar el entorno virtual:
   - Windows: `venv\Scripts\activate`
   - macOS/Linux: `source venv/bin/activate`
4. Instalar las dependencias: `pip install -r requirements.txt`

## Estructura del Proyecto
- `data/`: Contiene los archivos de datos utilizados en el proyecto.
- `notebooks/`: Incluye los notebooks de Jupyter con el análisis y modelos.
- `src/`: Contiene el código para la transformación de datos fuenta.
- `README.md`: Archivo de documentación del proyecto.
- `main.py`: Archivo principal de la API

## Uso y Ejecución
1. Se debe empesar ejecutando `TransformacionDatos.ipynb` en la carpeta `src/` para transformar los datos que se pueden enctonrar [aqui](#fuente-de-datos) .
2. El notebook procesara los datos y creara 6 nuevos archivos parquet dentro de la carpeta `data/`, uno llamado `dataset.parquet` que sera utilizado para el modelo de recomendacion.
3. Los otros 5 archivos:`dataset_1_2.parquet`,`dataset_3.parquet`,`dataset_4.parquet`,`dataset_5.parquet`,`dataset_6.parquet` seran utilizados para los endpoint de la API
4. Para crear el modelo de recomendación, ejecutar el notebook `ModeloRecomendacionpeliculas.ipynb` en la carpeta `notebooks/`.
5. Este notebook entrenara el modelo y creara el archivo `dataset_recomendaciones.parquet` en la carpeta `data/` para ser utilizado en el ultimo endpoint de la API.

## **Fuente de datos**
- + [Dataset](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5?usp=drive_link): Carpeta con los 2 archivos con datos que requieren ser procesados (movies_dataset.csv y credits.csv).
 
## Autores:
Este proyecto fue realizado por: Thomas Bracamonte.
<br/>

