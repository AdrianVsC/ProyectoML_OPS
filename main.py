from fastapi import FastAPI
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.preprocessing import LabelEncoder
app = FastAPI()

"""
def developer( desarrollador : str ): Cantidad de items y porcentaje de contenido Free 
por año según empresa desarrolladora.
"""
@app.get('/developer/{desarrollador}')

async def funcion1(desarrollador:str):
    
    df_desarrollador = pd.read_parquet(r"C:\Users\argui\OneDrive\Escritorio\ProyectoML_OPS\data\steam_games.parquet")
              # Filtrar el DataFrame por desarrollador
    df_desarrollador = df_desarrollador[df_desarrollador['developer'] == desarrollador].copy()

    # Verificar si el DataFrame filtrado está vacío
    if df_desarrollador.empty:
        print("No se encontraron juegos para el desarrollador especificado.")
        return None

    # Cambio el nombre de release_date a año
    df_desarrollador = df_desarrollador.rename(columns={'release_date':'año'})

    # Calcular el porcentaje de juegos gratuitos por año
    juegos_gratuitos_por_anio = df_desarrollador.groupby('año')['price'].apply(lambda x: (x == 0).mean() * 100).reset_index(name='porcentaje_juegos_gratuitos')

    # Contar la cantidad total de juegos por año
    cantidad_juegos_por_anio = df_desarrollador['año'].value_counts().reset_index()
    cantidad_juegos_por_anio.columns = ['año', 'cantidad_juegos']

    # Unir las tablas
    tabla_resultado = pd.merge(juegos_gratuitos_por_anio, cantidad_juegos_por_anio, on='año')
    tabla_resultado=tabla_resultado.reset_index(drop=True)

    resultado_dict = tabla_resultado.to_dict(orient='records')

    for registro in resultado_dict:
        registro['porcentaje_juegos_gratuitos'] = f"{registro['porcentaje_juegos_gratuitos']:.2f}%"


    return resultado_dict

@app.get('/Recomendacion_juego/{id_juego}')  
async def recomendacion_juego(id_juego:int):
    df = pd.read_parquet(r"C:\Users\argui\OneDrive\Escritorio\ProyectoML_OPS\data\recomendacion.parquet")

    # Verifica si existe el id.
    if id_juego not in df['item_id'].values:
        return "ID de juego no encontrado"
    
    # Vectoriza (convierte texto en valores numéricos).
    tfidf_vectorizer = TfidfVectorizer(stop_words='english')

    # Convierte 'genres' a cadena y lo codifica con LabelEncoder.
    label_encoder = LabelEncoder()
    df['genres_str'] = label_encoder.fit_transform(df['genres'].astype(str))

    # Combina 'genres_str', 'title', 'sentiment_analysis', y 'playtime_2weeks' en una nueva columna.

    # Esto es para generar vectores y comparar cosenos.
    df['combined_features'] = (
        df['genres_str'].astype(str) + ' ' +
        df['title'] + ' ' +
        df['sentiment_analysis'].astype(str) + ' ' +
        df['playtime_2weeks'].astype(str)
    )

    # Aplica el vectorizador a la nueva columna.
    tfidf_matrix = tfidf_vectorizer.fit_transform(df['combined_features'])

    # Escala 'sentiment_analysis' y 'playtime_2weeks'.
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[['sentiment_analysis', 'playtime_2weeks']])

    # Agrega las características escaladas.
    tfidf_matrix = pd.concat([pd.DataFrame(tfidf_matrix.toarray()), pd.DataFrame(scaled_features)], axis=1)

    # Calcula la similitud de coseno entre los juegos.
    cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

    # Obtiene el índice del juego en el DataFrame.
    idx = df[df['item_id'] == id_juego].index[0]

    # Obtiene las similitudes de coseno para el juego especificado.
    cosine_scores = list(enumerate(cosine_similarities[idx]))

    # Ordena los juegos por similitud de coseno. Cuanto más cercana a 1, más "parecido" es.
    cosine_scores = sorted(cosine_scores, key=lambda x: x[1], reverse=True)

    # Obtiene los índices de los 5 juegos recomendados (excluyendo el juego actual) por similitud.
    recommended_indices = [i[0] for i in cosine_scores[1:6]]  

    # Obtiene los títulos de los juegos recomendados.
    recommended_titles = df['title'].iloc[recommended_indices].tolist()
    return recommended_titles