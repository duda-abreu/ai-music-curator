import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import psycopg2

# Função para conectar ao banco de dados
def connect_db():
    return psycopg2.connect(
        dbname="recomendador_musicas",
        user="postgres",
        password="1234",
        host="localhost"
    )

# Função para carregar dados das músicas
def load_music_data():
    conn = connect_db()
    query = "SELECT id, titulo, artista, album, genero FROM Musicas"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Carregar dados e criar o modelo
music_df = load_music_data()
music_df['content'] = music_df['titulo'] + ' ' + music_df['artista'] + ' ' + music_df['genero'].apply(lambda x: ' '.join(x))
tfidf_vectorizer = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf_vectorizer.fit_transform(music_df['content'])

def recommend_songs(song_id, top_n=10):
    idx = music_df.index[music_df['id'] == song_id].tolist()[0]
    cosine_similarities = linear_kernel(tfidf_matrix[idx:idx+1], tfidf_matrix).flatten()
    related_indices = cosine_similarities.argsort()[:-top_n-1:-1]
    return music_df.iloc[related_indices]
