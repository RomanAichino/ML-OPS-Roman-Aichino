from fastapi import FastAPI
import pandas as pd
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
