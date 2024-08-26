import psycopg2

conn = psycopg2.connect(
    dbname="recomendador_musicas",
    user="postgres",
    password="1234",
    host="localhost",
    options="-c client_encoding=utf8"
)

# Criar um cursor
cursor = conn.cursor()

# Inserir dados de teste em Usuarios
cursor.execute("""
    INSERT INTO Usuarios (nome, email) VALUES
    ('Alice', 'alice@example.com'),
    ('Bob', 'bob@example.com');
""")

# Inserir dados de teste em Musicas
cursor.execute("""
    INSERT INTO Musicas (titulo, artista, album, genero) VALUES
    ('Song A', 'Artist A', 'Album A', 'Genre A'),
    ('Song B', 'Artist B', 'Album B', 'Genre B');
""")

# Inserir dados de teste em Historico
cursor.execute("""
    INSERT INTO Historico (usuario_id, musica_id, data_escuta) VALUES
    (1, 1, '2024-08-01 10:00:00'),
    (2, 2, '2024-08-02 15:00:00');
""")

# Inserir dados de teste em Preferencias
cursor.execute("""
    INSERT INTO Preferencias (usuario_id, musica_id, avaliacao) VALUES
    (1, 1, 5),
    (2, 2, 4);
""")

# Confirmar as alterações e fechar a conexão
conn.commit()
cursor.close()
conn.close()
