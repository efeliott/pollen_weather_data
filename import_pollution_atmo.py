import json
import psycopg2
from dotenv import load_dotenv
import os
from tqdm import tqdm

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pollution_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

JSON_FILE = "pollution_20220410_to_20250410.json"

def insert_data(conn, data):
    cursor = conn.cursor()
    inserted = 0

    for row in tqdm(data, desc="📥 Insertion depuis fichier JSON"):
        cursor.execute("""
            INSERT INTO pollution_data (
                mesure_id, date, valeur, validation,
                site_id, site_label, type_appareil_id, type_appareil_label,
                code_polluant, label_polluant, id_poll_ue, label_court_polluant,
                unite, label_unite, label_court_unite
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            row.get("mesure_id"),
            row.get("date"),
            row.get("valeur"),
            row.get("validation"),
            row.get("site_id"),
            row.get("site_label"),
            row.get("type_appareil_id"),
            row.get("type_appareil_label"),
            row.get("code_polluant"),
            row.get("label_polluant"),
            row.get("id_poll_ue"),
            row.get("label_court_polluant"),
            row.get("unite"),
            row.get("label_unite"),
            row.get("label_court_unite"),
        ))
        inserted += 1

    conn.commit()
    cursor.close()
    print(f"{inserted} lignes insérées en base.")

def main():
    print(f"Lecture du fichier JSON : {JSON_FILE}")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        content = json.load(f)

    data = content.get("data", [])
    print(f"🔍 {len(data)} enregistrements trouvés dans le fichier.")

    if not data:
        print("Aucune donnée à insérer.")
        return

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )

    insert_data(conn, data)
    conn.close()

if __name__ == "__main__":
    main()
