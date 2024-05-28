![banner1.jpg](imágenes/banner1.jpg)
# Proyecto Steam Maching Learning Operations + FASTAPI
## Contexto
Este proyecto simula el rol de un MLOps Engineer, es decir, la combinación de un Data Engineer y Data Scientist, para la plataforma multinacional de videojuegos Steam. Para su desarrollo, se entregan unos datos y se solicita un MVP que muestre una API deployada en un servicio en la nube y la aplicación de un modelo de Machine Learning para hacer recomendaciones de juegos.

# Primera Etapa: [ETL](/ETL/) 

 `Extracción de los datos:`

 *  Se nos fue entregados, datos json comprimidos en gz, por lo que se tuvo que realizar una descompresión de los datos manualmente.

 `Carga de los datos:`

 *  El siguiente trabajo fue el cargar los json a un DataFrame
 *  *output_steam_games.json*: Para este archivo json, bastó con usar pd.read_json para poder insertar los datos en un dataframe para su posterior análisis
 *  *australian_user_reviews.json*: Para poder usar este json se tuvo que recurrir a la librería *ast* debido a problemas de formato que dificultaban la lectura con pandas, cada línea se insertó en una lista para luego transformarla a un dataframe.
 *  *australian_users_items*: El caso de deste archivo fue similar al anteriormente mencionado, se aplicaron técnicas usando la librería ast para poder insertar los diccionarios en una lista para su posterior transformación en un DataFrame


 `Limpieza y transformación de los datos:`

 *  Una vez insertado *output_steam_games.json* en un dataframe, se procedió al análisis de la información dentro del dataframe, la cantidad de nulos por columna, los duplicados y nulos fueron eliminados, así como las columnas que no nos servía y a continuación se procedió a la transformación de los datos de la columna a tipos más livianos, también se extrajo el año de la columna 'release_date', finalmente, el dataframe final se exportó en un archivo comprimido [steam_games.parquet](/data/steam_games.parquet)

 *  Una vez insertado *australian_user_reviews.json* a un dataframe, se le realizó un trabajo de limpieza, transformación con el objetivo de optimizar las consultas y desanidado de la columna 'reviews', finalmente se exportó a un archivo [user_reviews.parquet](/data/user_reviews.parquet)

 * Finalmente insertado *australian_users*, se le realizó el mismo proceso de los anteriores, eliminando nulos, duplicados, columnas que no nos servirán, desanidado y finalmente comprimido [users_items.parquet](/data/users_items.parquet)


 # Segunda Etapa: Feature Engineering

 * En esta etapa, se utilizó los datos de user_reviews, para esto se reemplazó reviews por 0,1 o 2 según sea el caso pasando los textos de la columna 'review' que analiza el lenguaje natural y retorna valores de 0 a 2 dependiendo de si es neutral (1), negativo (0) o positivo (2)

 # Tercera Etapa: [EDA](/EDA/EDA.ipynb)

 * Se lleva a cabo el analisis exploratorio de los datos, identificando patrones y tendencias de los juegos y géneros mas recomendados por los usuarios, a parte de identificar outliers, el codigo utilizado se puede visualizar en EDA

 # Cuarta Etapa: [API](/main.py)

Para el desarrollo de la Api se utilizó FastAPI, este Framework permite que la API pueda ser consumida desde la WEB, esta consta de estos endpoints:

* *def developer( desarrollador : str )*: Cantidad de items y porcentaje de contenido Free por año según empresa desarrolladora.

# Quinta Etapa: ML

* El modelo se basa en la similitud del coseno, el modelo tiene una relación ítem-ítem, esto es, se toma un juego y en base a que tan similar es ese juego con el resto de los juegos se recomiendan similares: *def recomendacion_juego(id_juego:int)*

# Deployment

* Para el deploy de la API se seleccionó la plataforma Render, a continuacion el link donde se puede ver el funcionamiento de la API desplegado 
