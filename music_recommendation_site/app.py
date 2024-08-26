from flask import Flask, render_template, request, redirect, url_for, session
from ml_model import load_music_data, recommend_songs
from flask_bootstrap import Bootstrap
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
Bootstrap(app)

# Configurações do Spotify com OAuth
sp_oauth = SpotifyOAuth(
    client_id=os.getenv('SPOTIPY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI'),
    scope='user-library-read user-top-read user-read-playback-state'
)

def connect_db():
    return psycopg2.connect(
        dbname="recomendador_musicas",
        user="postgres",
        password="1234",
        host="localhost"
    )

# Função para obter preferências do usuário
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
def search_tracks(query):
    sp = spotipy.Spotify(auth_manager=sp_oauth)
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

@app.route('/')
def index():
    return render_template('index.html')

# Página de login
@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    print(f"Redirecionando para URL de autenticação: {auth_url}")
    return redirect(auth_url)

# Callback após autenticação
@app.route('/callback')
def callback():
    code = request.args.get('code')
    print(f"Código recebido: {code}") 
    if code:
        token_info = sp_oauth.get_access_token(code)
        session['token_info'] = token_info
        return redirect(url_for('recommend'))
    else:
        return 'Erro na autenticação', 400


# Página de recomendações
@app.route('/recommend', methods=['GET', 'POST'])
def recommend():
    token_info = session.get('token_info', None)
    if token_info:
        sp = spotipy.Spotify(auth=token_info['access_token'])

        music_df = load_music_data() 
        recommended_tracks = recommend_songs(music_df['id'].mode()[0])  

        return render_template('recommendations.html', tracks=recommended_tracks.to_dict(orient='records'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
