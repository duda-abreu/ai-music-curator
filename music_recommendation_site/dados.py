import psycopg2
import pandas as pd

def fetch_data():
    try:
        conn = psycopg2.connect(
            dbname="recomendador_musicas",
            user="postgres",
            password="1234",
            host="localhost"
        )
        query = "SELECT * FROM Musicas;"
        df = pd.read_sql(query, conn)
        conn.close()
        return df
    except Exception as e:
        print(f"Error in fetch_data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on error
