import psycopg2
from psycopg2 import sql

# Configurar a conexão com o banco de dados
def connect_to_db():
    try:
        conn = psycopg2.connect(
            dbname="recomendador_musicas",
            user="postgres",
            password="1234",
            host="localhost"
        )
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Criar tabelas no banco de dados
def create_tables(conn):
    try:
        with conn.cursor() as cursor:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS Usuarios (
                    id SERIAL PRIMARY KEY,
                    nome VARCHAR(100),
                    email VARCHAR(100)
                );

                CREATE TABLE IF NOT EXISTS Musicas (
                    id SERIAL PRIMARY KEY,
                    titulo VARCHAR(100),
                    artista VARCHAR(100),
                    album VARCHAR(100),
                    genero VARCHAR(50)
                );

                CREATE TABLE IF NOT EXISTS Historico (
                    id SERIAL PRIMARY KEY,
                    usuario_id INT REFERENCES Usuarios(id),
                    musica_id INT REFERENCES Musicas(id),
                    data_escuta TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS Preferencias (
                    id SERIAL PRIMARY KEY,
                    usuario_id INT REFERENCES Usuarios(id),
                    musica_id INT REFERENCES Musicas(id),
                    avaliacao INT
                );
            ''')
            conn.commit()
            print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
        conn.rollback()

# Função principal
def main():
    conn = connect_to_db()
    if conn:
        create_tables(conn)
        conn.close()

if __name__ == "__main__":
    main()
