import json
import psycopg2
from tqdm import tqdm

from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pollution_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

# Connexion Postgre
conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )
cursor = conn.cursor()

# Chargement du fichier JSON (local)
with open("bulletins_2.json", "r", encoding="utf-8") as f:
    data = json.load(f)

bulletins = data.get("values", [])
print(f"Nombre de bulletins chargés depuis le fichier : {len(bulletins)}")

# Requête d'insertion
total_inserted = 0
for row in tqdm(bulletins, desc="Insertion"):
    try:
        cursor.execute("""
            INSERT INTO pollen_bulletins (
                bulletin_date,
                station,
                designation,
                nom_latin,
                quantite,
                raep,
                type,
                commentaire,
                details
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            row.get("date_bulletin"),
            "Grand Lyon",  # ou autre station si dispo
            row.get("designation"),
            row.get("nom_latin"),
            row.get("quantite"),
            row.get("raep"),
            row.get("type"),
            row.get("commentaire"),
            json.dumps(row)
        ))
        total_inserted += 1
    except Exception as e:
        print("Erreur lors de l’insertion :", e)
        print("Ligne concernée :", row)

conn.commit()
cursor.close()
conn.close()

print(f"\nTerminé ! {total_inserted} bulletins insérés dans la base.")
