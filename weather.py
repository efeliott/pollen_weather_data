import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pollution_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

# Connexion à PostgreSQL
conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )
cursor = conn.cursor()
conn.commit()

# Lecture du fichier CSV avec virgules comme décimales
df = pd.read_csv("weather_20220810_to_20230810.csv", sep=';', encoding='utf-8', decimal=',', low_memory=False)

# Sélection des colonnes utiles par position : DATE = B(1), RR = C(2), TN = G(6), TX = K(10), TM = O(14), FFM = AG(32)
df_utiles = df.iloc[:, [1, 2, 6, 10, 14, 32]].copy()
df_utiles.columns = ["DATE", "RR", "TN", "TX", "TM", "FFM"]

# Nettoyage
df_utiles["DATE"] = pd.to_datetime(df_utiles["DATE"], format="%Y%m%d", errors="coerce")

# Préparation des lignes à insérer
records = df_utiles.to_records(index=False)
values = [
    (
        pd.to_datetime(r[0]).date(),
        float(r[1]) if not pd.isna(r[1]) else None,
        float(r[2]) if not pd.isna(r[2]) else None,
        float(r[3]) if not pd.isna(r[3]) else None,
        float(r[4]) if not pd.isna(r[4]) else None,
        float(r[5]) if not pd.isna(r[5]) else None,
    )
    for r in records if pd.notnull(r[0])
]


# Insertion dans la base
insert_query = '''
    INSERT INTO meteo_observations_lyon (
        date, precipitation_mm, temperature_min, 
        temperature_max, temperature_moy, vent_moyen
    ) VALUES %s
'''

execute_values(cursor, insert_query, values)
conn.commit()

cursor.close()
conn.close()

print("Données insérées avec succès et table réinitialisée.")
