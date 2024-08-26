from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from ml_model import recommend_songs, connect_db, load_music_data
import psycopg2

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap(app)

# Configurações do cliente Spotify
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id="2720b05d29404b55a21d2319ddf01526",
    client_secret="92774db7814043b6b1922a4878b383c1"
))

# Configurações do banco de dados
def connect_db():
    return psycopg2.connect(
        dbname="recomendador_musicas",
        user="postgres",
        password="1234",
        host="localhost"
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

# Função para buscar músicas no Spotify
# Atualizar função search_tracks para incluir a URL da imagem do álbum
def search_tracks(query):
    results = sp.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']
    return [{
        "id": track["id"],
        "titulo": track["name"],
        "artista": track["artists"][0]["name"],
        "album": track["album"]["name"],
        "genero": sp.artist(track["artists"][0]["id"])["genres"],
        "album_image_url": track["album"]["images"][0]["url"]  # URL da imagem do álbum
    } for track in tracks]


# Página inicial
@app.route('/')
def index():
    return render_template('index.html')

# Página de recomendações
@app.route('/recommend', methods=['POST'])
def recommend():
    user_id = request.form.get('user_id')
    preferences = get_user_preferences(user_id)

    if not preferences:
        query = "pop"
    else:
        genres = set()
        for _, avaliacao in preferences:
            if avaliacao >= 4:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT genero
                    FROM Musicas
                    WHERE id = %s
                """, (_,))
                result = cursor.fetchone()
                if result:
                    genres.update(result[0])
                cursor.close()
                conn.close()
        if genres:
            query = " OR ".join(f"genre:{genre}" for genre in genres)
        else:
            query = "pop"
    
# Carregar dados das músicas dentro da função recommend
    music_df = load_music_data()
    
    # Usando a música mais popular como base para recomendação
    recommended_tracks = recommend_songs(music_df['id'].mode()[0])  # substitua com ID adequado

    return render_template('recommendations.html', tracks=recommended_tracks.to_dict(orient='records'))

if __name__ == '__main__':
    app.run(debug=True)