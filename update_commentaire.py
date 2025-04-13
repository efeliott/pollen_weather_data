import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "pollution_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_SSLMODE = os.getenv("DB_SSLMODE", "require")

# Paramètres de connexion Railway
conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        sslmode=DB_SSLMODE
    )

cursor = conn.cursor()

target_id = 867  # ← l'ID de la ligne à mettre à jour
new_comment = "Risque très élevé à cause de la sécheresse."

cursor.execute("SELECT * FROM pollen_bulletins WHERE id = %s", (target_id,))
result = cursor.fetchone()

if result:
    print(f"igne trouvée (ID {target_id}) — mise à jour en cours...")

    # Étape 2 : Mise à jour du commentaire
    cursor.execute(
        "UPDATE pollen_bulletins SET commentaire = %s WHERE id = %s",
        (new_comment, target_id)
    )
    conn.commit()
    print("Commentaire mis à jour avec succès.")
else:
    print(f"Aucun enregistrement trouvé avec l'ID {target_id}.")

cursor.close()
conn.close()
