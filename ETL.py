#primero importamos las librerias que vamos a utilizar
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ast
import numpy as np

# importamos el dataset
df = pd.read_csv('movies_dataset.csv') 

#aqui creamos las dos funciones que vamos a utilizar para desanidar los datos de las columnas
#la primera es para datos que estén anidados en un diccionario y todo eso esté dentro de una lista
def convetidor1(obj):
    L= []
    if isinstance(obj, str) and '{' in obj:
        for i in ast.literal_eval(obj):
            L.append(i['name'])
        return L
    
#la segunda es para datos que estén anidados en un diccionario
def convetidor2(obj):
    if isinstance(obj, str) and '{' in obj:
        dic = ast.literal_eval(obj)
        return dic['name']
    
#aquí aplicamos las dos funciones anteriores en las columnas que lo requieran
df['belongs_to_collection'] = df['belongs_to_collection'].apply(convetidor2)
df['genres'] = df['genres'].apply(convetidor1)
df['production_companies'] = df['production_companies'].apply(convetidor1)
df['production_countries'] = df['production_countries'].apply(convetidor1)
df['spoken_languages'] = df['spoken_languages'].apply(convetidor1)

#aqui vamos a rellenar con 0 las filas que sean nulas de la columna revenue y budget
df['revenue'] = df['revenue'].fillna(0) 
df['budget'] = df['budget'].fillna(0)

#aquí eliminamos lo valores nulos de la columna 'release_date'
df = df.dropna(subset=['release_date']) 

# funcion que recorre las columna y verifica cada valor
import re
regex = re.compile(r'^\d{4}-\d{2}-\d{2}$')
def validar_fecha(fecha):
    if regex.match(fecha):
        return fecha
    else:
        return None

#aplicamos la funcion anterior a la columna release_date
df['release_date'] = df['release_date'].apply(validar_fecha) 

#aquí volvemos a eliminar lo valores nulos de la columna 'release_date'
df = df.dropna(subset=['release_date']) 

#aquí verificamos que no hayan quedado valores nulos en la misma
df['release_date'].isnull().sum() 

#esta es una función que me dio ChatGPT para verificar que todos las fechas de release_date 
# estén en la forma (AAAA - MM - DD)
if df['release_date'].str.match(r'\d{4}-\d{2}-\d{2}').all():
    print("Todas las fechas tienen la forma AAAA-MM-DD")
else:
    print("No todas las fechas tienen la forma AAAA-MM-DD")

#aquí añadimos la columna release_year
df.insert(10, 'release_year', None) 

#aquí rellenamos release_year solo con los años de release_date
df['release_year'] = df['release_date'].str.split('-', expand=True)[0]  

#aquí pasamos todos los datos a float, ya que me daba error por algún str
df['revenue'] = pd.to_numeric(df['revenue'], errors='coerce') 
df['budget'] = pd.to_numeric(df['budget'], errors='coerce')

#aquí añadimos la columna return
df['return'] = np.where(np.logical_or(df['revenue'] == 0, df['budget'] == 0), 0, df['revenue'] / df['budget']) 

# dropeamos las columnas que no vamos a usar
df = df.drop('video', axis=1)
df = df.drop('imdb_id', axis=1)
df = df.drop('adult', axis=1)
df = df.drop('original_title', axis=1)
df = df.drop('poster_path', axis=1)
df = df.drop('homepage', axis=1)

#exportamos el dataset con los cambios pedidos ya realizados
df.to_csv('processed_data.csv')

#ahora crearemos el dataset para un modelo de recomendacion

df = df.drop('id', axis=1)
df = df.drop('release_year', axis=1)
df = df.drop('production_countries', axis=1)
df = df.drop('release_date', axis=1)
df = df.drop('revenue', axis=1)
df = df.drop('status', axis=1)
df = df.drop('vote_count', axis=1)
df = df.drop('overview', axis=1)
df = df.drop('budget', axis=1)
df = df.drop('tagline', axis=1)
df = df.drop('return', axis=1)

df = df.dropna()
df = df[0:5000]

df.to_csv('ML_data.csv')