import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sqlalchemy import create_engine
import psycopg2

def connect_db():
    return create_engine('postgresql://postgres:1234@localhost/recomendador_musicas')

def load_music_data():
    engine = connect_db()
    query = "SELECT id, titulo, artista, album, genero FROM Musicas"
    try:
        df = pd.read_sql(query, engine)
        print(df.head())  # Verifica os dados carregados
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        df = pd.DataFrame()
    return df

# Criação do DataFrame e modelo de recomendação
music_df = load_music_data()
music_df['content'] = music_df['titulo'].fillna('') + ' ' + music_df['artista'].fillna('') + ' ' + music_df['genero'].fillna('').astype(str)
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(music_df['content'])

def recommend_songs(song_id, top_n=10):
    if song_id not in music_df['id'].values:
        print(f"ID da música {song_id} não encontrado.")
        return pd.DataFrame()
    
    idx = music_df.index[music_df['id'] == song_id].tolist()[0]
    cosine_similarities = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
    related_indices = cosine_similarities.argsort()[:-top_n-1:-1]
    return music_df.iloc[related_indices]