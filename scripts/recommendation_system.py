# scripts/recommendation_system.py

import psycopg2
from spotify_api import get_track_info, search_tracks

# Configurações de conexão com o banco de dados
def connect_db():
    return psycopg2.connect(
        dbname="recomendador_musicas",
        user="postgres",
        password="1234",
        host="localhost",
        options="-c client_encoding=utf8"
    )

# Função para obter preferências do usuário do banco de dados
def get_user_preferences(user_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT musica_id, avaliacao
        FROM Preferencias
        WHERE usuario_id = %s
    """, (user_id,))
    preferences = cursor.fetchall()
    cursor.close()
    conn.close()
    return preferences

# Função para recomendar músicas com base nas preferências dos usuários
def recommend_music(user_id):
    preferences = get_user_preferences(user_id)
    
    if not preferences:
        print("Nenhuma preferência encontrada. Realizando busca genérica.")
        query = "pop"
        recommended_tracks = search_tracks(query)
    else:
        print("Encontradas preferências do usuário. Realizando busca personalizada.")
        genres = set()
        conn = connect_db()
        cursor = conn.cursor()

        for music_id, avaliacao in preferences:
            if avaliacao >= 4:  # Apenas músicas com alta avaliação
                cursor.execute("""
                    SELECT genero
                    FROM Musicas
                    WHERE id = %s
                """, (music_id,))
                result = cursor.fetchone()
                if result:
                    genres.update(result[0])  # Gêneros podem estar em formato de lista

        cursor.close()
        conn.close()

        if genres:
            query = " OR ".join(f"genre:{genre}" for genre in genres)
        else:
            query = "pop"  # Fallback se não houver gêneros

        recommended_tracks = search_tracks(query)

    for track in recommended_tracks:
        info = get_track_info(track["id"])
        print(f"Title: {info['titulo']}, Artist: {info['artista']}, Album: {info['album']}, Genres: {info['genero']}")

if __name__ == "__main__":
    user_id = 2  # Substitua com o ID do usuário desejado, por exemplo, Bob
    recommend_music(user_id)
