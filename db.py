# app/database.py (ou traafdata/database.py)

from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base # Base est déjà dans models.py
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv # <--- AJOUTER CET IMPORT

load_dotenv() # <--- APPELER load_dotenv() ICI, AVANT DE LIRE LES VARIABLES

DB_USER = os.getenv("DB_USER") # Plus besoin de valeur par défaut ici si .env est bien chargé
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Vérification que les variables sont bien chargées (pour le débogage)
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    print("ERREUR: Toutes les variables d'environnement de base de données ne sont pas définies.")
    print(f"DB_HOST: {DB_HOST}") # Pour voir quelle variable est None
    # Vous pourriez même lever une exception ici pour arrêter le démarrage de l'app
    # raise EnvironmentError("Variables d'environnement de base de données manquantes.")

SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Importer Base depuis votre fichier models.py
from models import Base # Si database.py et models.py sont dans le même dossier/package
# Ou ajustez le chemin d'import : from traafdata.models import Base

# Dépendance pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()