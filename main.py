#comenzamos importando las librerias a utilizar
from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import sklearn
import ast
import requests

#definimos app para fastapi
app = FastAPI()

#primera función: elegimos una película, y la funcion nos retornará la duración en minutos de la misma y el año estreno
#hay que tener en cuenta que de haber mas de una pelicula con ese nombre, retornara la que se haya estrenado primero
@app.get("/peliculas_duracion/{pelicula}")
def peliculas_duracion(pelicula:str):
    #importamos el dataset y quitamos lo nulos de la columna que utilizaremos como parametro del titulo
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['title'])
    #creamos un dataset con las filas las cuales el titulo coincida con el elegido, de no haber ninguno se retornara pelicula no valida
    df_pelicula = df.loc[df['title'] == pelicula]
    if len(df_pelicula) > 0:
        primer_estreno = df_pelicula.iloc[0]['release_year']
        runtime = df_pelicula.iloc[0]['runtime']
        #creo un ciclo para recorer el dataset y verificar una por una cual es la que primero se haya estrenado
        for i in range(0, len(df_pelicula['release_year'])-1):
            if df_pelicula.iloc[i]['release_year'] < primer_estreno: 
                primer_estreno = int(df_pelicula.iloc[i]['release_year'])
                runtime = int(df_pelicula.iloc[i]['runtime'])
        return {'Título':pelicula, 'duración en minutos':int(runtime), 'anio de estreno':int(primer_estreno)}
    else: return {'Pelicula no valida':pelicula}

#segunda función: elegimos el nombre de una franquicia, y la función nos retornará la cantidad de peliculas que realizó 
#junto con su ganancia total y el promedio por pelicula
@app.get("/franquicia/{franquicia_nom}")
def franquicia(franquicia_nom:str):
    #importamos el dataset y quitamos lo nulos de la columna que utilizaremos como parametro del nombre de la franquicia
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['belongs_to_collection'])
    #creamos un dataset donde apareceran las filas de peliculas hechas por la franquicia elegida, si es 0 retornara franquicia no valida
    peliculass = df.loc[df['belongs_to_collection'] == franquicia_nom]
    if len(peliculass) > 0:
        cantidad_peliculas = len(peliculass['belongs_to_collection'])
        ganancia = peliculass['revenue'].sum()
        return {'Franquicia':franquicia_nom, 'cantidad de peliculas':int(cantidad_peliculas), 'ganancia total':int(ganancia) , 'ganancia promedio por pelicula':round(float(ganancia / cantidad_peliculas),3)}
    else: return {'Franquicia no valida':franquicia_nom}

#tercer función: elegimos un país y la función retornara la cantidad de peliculas creadas en ese país
@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais:str):
    #importamos el dataset y quitamos lo nulos de la columna que utilizaremos como parametro del país
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    #creamos el dataset con las filas de peliculas hechas en el país elegido, de ser 0 se retornara pais no valido o sin peliculas
    respuesta = int(df['production_countries'].str.count(pais).sum())
    if respuesta > 0: return {'Pais':pais, 'cantidad de peliculas':int(respuesta)}
    else: return {'Este pais no tiene peliculas o no esta disponible':pais}

#cuarta función: elegimos una productora y la función retornara la cantidad de peliculas junto con su ganancia total 
@app.get("/productoras_exitosas/{productora}")
def productoras_exitosas(productora:str):
    #importamos el dataset y quitamos lo nulos de la columna que utilizaremos como parametro de la productora
    df = pd.read_csv('processed_data.csv')
    df = df.dropna(subset=['production_companies']) 
    #creamos el dataset donde apareceran las filas de peliculas realizadas por tal productora, de ser 0 se retornara productora no valida
    df_productora = df[df['production_companies'].str.contains(productora)]
    if len(df_productora) > 0:
        cantidad = len(df_productora)
        ganancia = df_productora['revenue'].sum()
        return {'Productora':productora, 'ganancia total':int(ganancia), 'cantidad de peliculas':int(cantidad)}
    else: {'Productora no valida':productora}

#quinta función: elegimos un idioma (sus iniciales) y nos retornara la cantidad de peliculas hechas originamente en ese idioma
@app.get("/peliculas_idioma/{idioma}")
def peliculas_idioma(idioma:str):
    #importamos el dataset y quitamos lo nulos de la columna que utilizaremos como parametro del idioma
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['spoken_languages'])
    #cremos el dataset con las filas de peliculas realizadas originalmente en ese idioma, de ser 0 se retornara idioma no disponible
    df_idiomas = df.loc[df['original_language'] == idioma]
    if int(len(df_idiomas)) == 0: return {'idioma no disponible':idioma}
    else: return {'idioma':idioma, 'cantidad de peliculas':int(len(df_idiomas))}

#sexta función: elegimos el titulo de una película y la función nos recomendará 5 peliculas a partir de la elegida
#los puntos que se utilizan para recomendar son el titulo, generos, puntación y franquicia
@app.get("/recomendacion/{titulo}")
def recomendacion(titulo:str):
    #importamos el dataset creado especificamente para esta función
    df = pd.read_csv('ML_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    #separamos los generos
    generos = df['genres'].str.join(sep='|').str.get_dummies()
    pelicula_generos = df.loc[df['title'] == titulo]['genres'].values
    #controlamos que la pelicula se encuentre en el dataset
    if len(pelicula_generos) == 0:
        a = '<3'
        return {"No se encontró la película ":titulo, 'ten en cuenta que el dataset es la mitad de el original por la cantidad de recursos consumidos en render': a}
    
    #calculamos la similitud de generos entre peliculas
    pelicula_generos = ast.literal_eval(pelicula_generos[0])
    df['genres_similar'] = df['genres'].apply(lambda x: len(set(pelicula_generos) & set(ast.literal_eval(x))) / len(set(pelicula_generos) | set(ast.literal_eval(x))))
    #creamos 'Misma_franquicia' para ver si las películas pertenecen a la misma franquicia. 
    #esto se determina verificando si el título seleccionado se encuentra en el título de otras películas,
    #aunque no es 100 porciento confiable, ya que podria no tener el mismo nombre.
    df['Misma_franquicia'] = df['title'].apply(lambda x: 1 if titulo.lower() in x.lower() else 0)
    features_df = pd.concat([generos, df['vote_average'], df['genres_similar'], df['Misma_franquicia']], axis=1)

    #Se utiliza el algoritmo de k-NN para encontrar películas similares.
    k = 5
    kn = NearestNeighbors(n_neighbors=k+1, algorithm='auto')
    kn.fit(features_df)
    indices = kn.kneighbors(features_df.loc[df['title'] == titulo])[1].flatten()
    # Se crea una lista de películas recomendadas a partir de los indices encontrados en el paso anterior.
    peliculas_recomendadas = list(df.iloc[indices]['title'])
    peliculas_recomendadas = sorted(peliculas_recomendadas, key=lambda x: (df.loc[df['title'] == x]['Misma_franquicia'].values[0], df.loc[df['title'] == x]['vote_average'].values[0], df.loc[df['title'] == x]['genres_similar'].values[0]), reverse=True)
    peliculas_recomendadas = [movie for movie in peliculas_recomendadas if movie != titulo]
    return {'Pelicula':titulo, 'recomendacion': peliculas_recomendadas}