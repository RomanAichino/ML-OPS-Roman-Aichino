from fastapi import FastAPI
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import sklearn
import ast
import requests

app = FastAPI()

@app.get("/peliculas_duracion/{pelicula}")
def peliculas_duracion(pelicula:str):
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['title'])
    
    df_pelicula = df.loc[df['title'] == pelicula]
    if len(df_pelicula) > 0:
        primer_estreno = df_pelicula.iloc[0]['release_year']
        runtime = df_pelicula.iloc[0]['runtime']
        for i in range(0, len(df_pelicula['release_year'])-1):
            if df_pelicula.iloc[i]['release_year'] < primer_estreno: 
                primer_estreno = int(df_pelicula.iloc[i]['release_year'])
                runtime = int(df_pelicula.iloc[i]['runtime'])
        return {'Título':pelicula, 'duración en minutos':int(runtime), 'anio de estreno':int(primer_estreno)}
    else: return {'Pelicula no valida':pelicula}

@app.get("/franquicia/{franquicia_nom}")
def franquicia(franquicia_nom:str):
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['belongs_to_collection'])
    peliculass = df.loc[df['belongs_to_collection'] == franquicia_nom]
    if len(peliculass) > 0:
        cantidad_peliculas = len(peliculass['belongs_to_collection'])
        ganancia = peliculass['revenue'].sum()
        return {'Franquicia':franquicia_nom, 'cantidad de peliculas':int(cantidad_peliculas), 'ganancia total':int(ganancia) , 'ganancia promedio por pelicula':round(float(ganancia / cantidad_peliculas),3)}
    else: return {'Franquicia no valida':franquicia_nom}

@app.get("/peliculas_pais/{pais}")
def peliculas_pais(pais:str):
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    respuesta = int(df['production_countries'].str.count(pais).sum())
    if respuesta > 0: return {'Pais':pais, 'cantidad de peliculas':int(respuesta)}
    else: return {'Este pais no tiene peliculas o no esta disponible':pais}

@app.get("/productoras_exitosas/{productora}")
def productoras_exitosas(productora:str):
    df = pd.read_csv('processed_data.csv')
    df = df.dropna(subset=['production_companies']) 
    df_productora = df[df['production_companies'].str.contains(productora)]
    if len(df_productora) > 0:
        cantidad = len(df_productora)
        ganancia = df_productora['revenue'].sum()
        return {'Productora':productora, 'ganancia total':int(ganancia), 'cantidad de peliculas':int(cantidad)}
    else: {'Productora no valida':productora}

@app.get("/peliculas_idioma/{idioma}")
def peliculas_idioma(idioma:str):
    df = pd.read_csv('processed_data.csv')
    df = df.drop('Unnamed: 0', axis=1)
    df = df.dropna(subset=['spoken_languages'])
    df_idiomas = df.loc[df['original_language'] == idioma]
    if int(len(df_idiomas)) == 0: return {'idioma no disponible':idioma}
    else: return {'idioma':idioma, 'cantidad de peliculas':int(len(df_idiomas))}

@app.get("/recomendacion/{titulo}")
def recomendacion(titulo:str):
    df = pd.read_csv('ML_data.csv')
    df = df.drop('Unnamed: 0', axis=1)

    generos_df = df['genres'].str.join(sep='|').str.get_dummies()
    
    selected_genres = df.loc[df['title'] == titulo]['genres'].values
    if len(selected_genres) == 0:
        return {"No se encontró la película ":titulo}
    #calculamos la similitud de generos entre peliculas
    selected_genres = ast.literal_eval(selected_genres[0])
    df['genre_similarity'] = df['genres'].apply(lambda x: len(set(selected_genres) & set(ast.literal_eval(x))) / len(set(selected_genres) | set(ast.literal_eval(x))))
    
    #Se crea una variable binaria llamada 'same_series' que indica si las películas pertenecen a la misma serie. 
    #Esto se determina verificando si el título seleccionado se encuentra en el título de otras películas.
    df['same_series'] = df['title'].apply(lambda x: 1 if titulo.lower() in x.lower() else 0)
    
   
    features_df = pd.concat([generos_df, df['vote_average'], df['genre_similarity'], df['same_series']], axis=1)
#Se utiliza el algoritmo de k-NN (k-Nearest Neighbors) para encontrar películas similares.
#  Se establece el valor de k en 6. Se entrena el modelo k-NN utilizando el dataframe features_df. 
# Luego, se encuentra el índice de las películas más similares a la película seleccionada utilizando
#  el método kneighbors y se guarda en la variable indices.
    
    k = 6
    knn = NearestNeighbors(n_neighbors=k+1, algorithm='auto')
    knn.fit(features_df)
    indices = knn.kneighbors(features_df.loc[df['title'] == titulo])[1].flatten()
    recommended_movies = list(df.iloc[indices]['title'])

    #selected_score = df.loc[df['title'] == selected_title]['vote_average'].values[0]
    recommended_movies = sorted(recommended_movies, key=lambda x: (df.loc[df['title'] == x]['same_series'].values[0], df.loc[df['title'] == x]['vote_average'].values[0], df.loc[df['title'] == x]['genre_similarity'].values[0]), reverse=True)
    recommended_movies = [movie for movie in recommended_movies if movie != titulo]
   # Se crea una lista de películas recomendadas a partir de los índices encontrados en el paso anterior.
   # La lista contiene los títulos de las películas correspondientes a los índices.
    return recommended_movies