Buenas, soy Roman Aichino y este es mi proyecto sobre Ingenieria de datos para el bootcamp 'SoyHenry'.

El proyecto trata sobre la creación de un servicio de consulta sobre un dataset de peliculas, mi rol empieza siendo el de un desarrollador ETL, donde recibo unos datos bastante desprolijos y los acomodo con las indicaciónes recibidas desde el departamento de analisis de datos para luego exportarlo en dos datasets (uno para las funciones de consulta y otro para un futuro sistema de recomendación); una vez terminada esa parte, mi rol avanza hacia un MLOps en donde mi tarea principal es desarrollar un sistema de recomendación de peliculas, no sin antes levantar una API utilizando la plataforma de render.com y crear 5 funciones en donde podremos consultar datos de uno de los dataset ya modificados.

Aclaración: sé que en las indicaciónes me pedian una sexta función, pero como no me salió a la primera decidí no hacerlo y ocupar el tiempo en otros aspectos del proyecto.

Siguiendo con la explicación, debo mencionar que para la preparación del dataset utilizado para el sistema de recomendación tuve que ocupar el rol de analista de datos, durante ese tramo fuí guíandome en graficos y otros aspectos como la calidad de las columnas(que no haya tantos valores nulos), al final decidí que la mayoría de las columnas no me aportaban nada a la hora de recomendar una película, por lo cual terminé por usar solo unas 4 o 5 columnas de todo el dataset. Una vez terminado el set de datos para el sistema, me incliné por usar el sistema K-Neighbors ya que me parecía el mas simple para esto y porque compañeros con mas conocimientos del tema me lo recomendaron.

Video explicativo: https://www.youtube.com/watch?v=6Bi1hk0J6qo

Render: https://ml-ops-roman-aichino.onrender.com/

Repocitorio: https://github.com/RomanAichino/ML-OPS-Roman-Aichino

Descripción los cada archivo:
ETL.py: aquí realice la extracción, todas las modificaciones e importación de los dos dataset.
main.py: aquí estan las 5 funciónes de consulta y el sistema de recomendación de peliculas en forma de una sexta función.
movies_dataset.csv: es el dataset original, sin ninguna modificación.
processed_data.csv: es el dataset con las moodificaciones realizadas, listo para utilizar en las 5 funciones de consulta.
ML_data.csv: es el dataset utilizado para el sistema de recomendación.
requirements.txt: las librerias utilizadas con sus respectivas versiones.
EDA.ipynb: aquí se hayan unos graficos que utilicé para el analisis de datos.