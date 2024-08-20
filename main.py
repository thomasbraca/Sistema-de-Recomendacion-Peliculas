from fastapi import FastAPI, HTTPException
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()

def cantidad_filmaciones_meses(df, mes):
    """
    Se ingresa un mes en idioma Español. 
    Devuelve la cantidad de películas que fueron estrenadas en el mes consultado en la totalidad del dataset.
    """

    meses = {
        "enero" : "January",
        "febrero" : "February",
        "marzo"  : "March",
        "abril" : "April",
        "mayo" : "May",
        "junio" : "June",
        "julio" : "July",
        "agosto" : "August",
        "septiembre" : "September",
        "octubre" : "October",
        "noviembre" : "November",
        "diciembre" : "December"
    }

    if mes.lower() in meses:
        total = len(df[pd.DatetimeIndex(df['release_date']).strftime("%B")==meses[mes.lower()]])
        result = {
        'Para el mes': mes,
        'Se estrenaron esta cantidad de peliculas': total
    }
        len(df[pd.DatetimeIndex(df['release_date']).strftime("%B")==meses[mes.lower()]])
    else:
        result = {
        'El texto ingresado no es un mes': mes
    }
    
    return result

def cantidad_filmaciones_dias(df, dia ):
    """
    Se ingresa un día en idioma Español. 
    Debe devolver la cantidad de películas que fueron estrenadas en día consultado en la totalidad del dataset.
    """

    dias = {
        "lunes" : 1,
        "martes" : 2,
        "miercoles"  : 3,
        "jueves" : 4,
        "viernes" : 5,
        "sabado" : 6,
        "domingo" : 7
    }

    if dia.lower() in dias:
        total = len(df[pd.DatetimeIndex(df['release_date']).day_of_week==dias[dia.lower()]])
        result = {
        'Para el dia': dia,
        'Se estrenaron esta cantidad de peliculas': total
    }
        len(df[pd.DatetimeIndex(df['release_date']).day_of_week==dias[dia.lower()]])
    else:
        result = {
        'El texto ingresado no es un dia': dia
    }
    
    return result


def score_titulos(df, titulo_de_la_filmación ):
    if (not (df.loc[df['title'].str.lower() == titulo_de_la_filmación.lower()].empty)):
        df_filter = df.loc[df['title'].str.lower() == titulo_de_la_filmación.lower()]
        titulo = df_filter['title'].iloc[0]
        anio = df_filter['release_year'].iloc[0]
        popularity = df_filter['popularity'].iloc[0]

        result = {
        'La pelicula': titulo,
        'Se estrenaron een el año': anio,
        'Y tiene una popularidad de': popularity
    }
    else:
        result = {
        'El texto ingresado no es un titulo': titulo_de_la_filmación
    }

    return result

def votos_titulos(df, titulo_de_la_filmación):
    
    df_filter = df.loc[df['title'].str.lower() == titulo_de_la_filmación.lower()]
    if not df_filter.empty:
        titulo = df_filter['title'].iloc[0]
        votos = df_filter['vote_count'].iloc[0]
        if votos>2000:
            anio = df_filter['release_year'].iloc[0]
            puntaje  = df_filter['vote_average'].iloc[0]

            result = {
            'La pelicula': titulo,
            'Se estrenaron een el año': anio,
            'Tiene un total de votaciones': votos,
            'Con un promedio de puntaje': puntaje
            }
        else:
            result = {
            'La pelicula': titulo,
            'Tiene menos de 2000 votaciones': votos 
            }
    else:
        result = {
        'El texto ingresado no es un titulo': titulo_de_la_filmación
    }

    return result


def get_actors(df, nombre_actor):
    df_filter = df[df['cast'].apply(lambda x: nombre_actor.lower() in x.lower())]
    if not df_filter.empty:
        cantidad = len(df_filter.index)
        total_retorno = df_filter['return'].sum()
        promedio_retorno = df_filter['return'].mean()

        result = {
            'El actor': nombre_actor,
            'Actuo en esta cantidad de peliculas': cantidad,
            'Tuvo un total de retorno de': total_retorno,
            'Con un promedio de retorno por pelicula': promedio_retorno
            }
        

    else:
        result = {
        'El texto ingresado no es un actor': nombre_actor
    }
        
    return result


def get_directors(df, nombre_director):
    df_filter = df[df['Director'].apply(lambda x: nombre_director.lower() in x.lower())]
    if not df_filter.empty:
        cantidad = len(df_filter.index)
        total_retorno = df_filter['return'].sum()
        promedio_retorno = df_filter['return'].mean()

        result = {
            'El director': nombre_director,
            'Dirijio en esta cantidad de peliculas': cantidad,
            'Tuvo un total de retorno de': total_retorno,
            'Con un promedio de retorno por pelicula': promedio_retorno,
            'Listado de peliculas' : df_filter[['title','release_date','budget','revenue','return']].to_dict(orient='records')
            }
        

    else:
        result = {
        'El texto ingresado no es un director': nombre_director
    }
        
    return result

def recomendaciones(df, titulo_de_la_filmación):
     df_filter = df.loc[df['title'].str.lower() == titulo_de_la_filmación.lower()]
     if not df_filter.empty:
         result = {
            'Primera recomendacion': df_filter['rec1'].iloc[0],
            'Segunda recomendacion': df_filter['rec2'].iloc[0],
            'Tercera recomendacion': df_filter['rec3'].iloc[0],
            'Cuarta recomendacion': df_filter['rec4'].iloc[0],
            'Quinta recomendacion': df_filter['rec5'].iloc[0]
            }
     else:
         result ={
              'El texto ingresado no es una pelicula': titulo_de_la_filmación
         }
     return result


@app.get("/Cantidad filaciones por mes")
def cantidad_filmaciones_mes(mes: str):
    """
    Obtiene la cantidad de peliculas que fueron estrenadas en el mes ingresado.
    El mes debe ser ingresado en español, por ejemple: "Enero"
    """

    try:
        df = pd.read_parquet("./data/dataset_1_2.parquet")

        result = cantidad_filmaciones_meses(df,mes)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    

@app.get("/Cantidad filmaciones por dia")
def cantidad_filmaciones_dia(dia: str):
    """
    Obtiene la cantidad de peliculas que fueron estrenadas en el dia de la semana ingresado.
    El dia debe ser ingresado en español, por ejemple: "Lunes"
    """

    try:
        df = pd.read_parquet("./data/dataset_1_2.parquet")

        result = cantidad_filmaciones_dias(df,dia)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    


@app.get("/Popularidad por titulo")
def score_titulo(titulo: str):
    """
    Obtiene el año de estreno y su popularidad a partir del titulo de la pelicula
    """

    try:
        df = pd.read_parquet("./data/dataset_3.parquet")

        result = score_titulos(df,titulo)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    
@app.get("/Votos por titulo")
def votos_titulo(titulo: str):
    """
    Obtiene el año de estreno, cantidad de votos y promedio de dichos votos a partir del titulo de la pelicula.
    Si la pelicula tuvo menos de 2000 no devuelve ningun valor.
    """

    try:
        df = pd.read_parquet("./data/dataset_4.parquet")

        result = votos_titulos(df,titulo)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")
    

@app.get("/Exito de actor")
def get_actor(nombre_actor: str):
    """
    Obtiene el exito de un actor a base de cuanto retorno tuvo en sus peliculas, tambien nos dice en cuantas peliculas actuo
    """

    try:
        df = pd.read_parquet("./data/dataset_5.parquet")

        result = get_actors(df,nombre_actor)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")

@app.get("/Exito por director")
def get_director(nombre_director: str):
    """
    Obtiene el exito de un director a base de cuanto retorno tuvo en sus peliculas.
    Tambien nos da un listado de todas las peliculas que dirigio
    """

    try:
        df = pd.read_parquet("./data/dataset_6.parquet")

        result = get_directors(df,nombre_director)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")


@app.get("/Sistema de recomendacion")
def recomendacion(titulo):
    """
    Devuelve 5 peliculas de recomendacion a base de una 
    """

    try:
        df = pd.read_parquet("./data/dataset_recomendaciones.parquet")

        result = recomendaciones(df,titulo)

        return JSONResponse(content=jsonable_encoder(result), media_type="application/json")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Archivo Parquet no encontrado, revisa si la ruta del archivo es correcta")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al leer el archivo Parquet: {str(e)}")