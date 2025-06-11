# load_initial_data.py
import os
import csv
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import SessionLocal, engine

Base = declarative_base()

# --- Définition dynamique des modèles GTFS ---
def create_gtfs_model(table_name: str, columns: list):
    """Crée dynamiquement un modèle SQLAlchemy pour une table GTFS."""
    attrs = {'__tablename__': table_name}
    for column in columns:
        column_name = column.lower()  # Convertir le nom de colonne en minuscules par convention
        # Essayer de deviner le type de la colonne (simple pour l'instant)
        if 'id' in column_name or '_id' in column_name or 'code' in column_name or 'date' in column_name or 'time' in column_name or 'url' in column_name or 'name' in column_name or 'desc' in column_name or 'headsign' in column_name or 'email' in column_name or 'lang' in column_name or 'version' in column_name or 'type' in column_name or 'currency' in column_name:
            attrs[column_name] = Column(String, primary_key='id' in column_name and '_id' not in column_name, index='id' in column_name or '_id' in column_name)
        elif 'lat' in column_name or 'lon' in column_name or 'dist' in column_name or 'price' in column_name or 'index' in column_name or 'length' in column_name:
            attrs[column_name] = Column(Float)
        else:
            attrs[column_name] = Column(Integer)
    return type(table_name.capitalize(), (Base,), attrs)

# --- Fonctions utilitaires ---
CSV_FILES_DIR = "data"
CSV_DELIMITER = ","

def create_tables_if_not_exists():
    print("Tentative de création des tables de la base de données...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Tables de la base de données créées ou déjà existantes.")
    except Exception as e:
        print(f"Erreur lors de la création des tables : {e}")
        raise

def load_csv_file_to_dict(file_path: str):
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=CSV_DELIMITER)
            for row in reader:
                cleaned_row = {k.lower(): (v if v is not None and v.strip() != '' else None) for k, v in row.items()} # Convertir les clés en minuscules
                data.append(cleaned_row)
        return data
    except FileNotFoundError:
        print(f"Erreur : Fichier '{file_path}' non trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier CSV '{file_path}' : {e}")
        return None

def insert_data(db, model, data: list[dict], filename: str):
    rows_inserted_count = 0
    try:
        for row_data in data:
            try:
                instance = model(**row_data)
                db.add(instance)
                rows_inserted_count += 1
            except IntegrityError as e:
                db.rollback()
                primary_key_values = {pk.name: row_data.get(pk.name) for pk in model.__mapper__.primary_key}
                print(f"  -> Doublon détecté dans '{filename}' pour la clé primaire: {primary_key_values}. Ligne ignorée. Erreur: {e}")
                db = SessionLocal() # Nouvelle session
            except Exception as e:
                db.rollback()
                print(f"  -> Erreur lors de l'insertion dans '{filename}': {row_data}. Erreur: {e}")
                db = SessionLocal() # Nouvelle session
        db.commit()
        print(f"  -> Inséré {rows_inserted_count} lignes dans la table '{model.__tablename__}' depuis '{filename}'.")
        return rows_inserted_count
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Erreur générale lors de l'insertion des données de '{filename}': {e}")
        return 0
    finally:
        pass # La session est gérée dans la boucle principale

if __name__ == "__main__":
    print(f"Démarrage du script de chargement dynamique de données depuis '{CSV_FILES_DIR}'...")

    create_tables_if_not_exists()
    total_rows_successfully_inserted = 0

    for filename in os.listdir(CSV_FILES_DIR):
        if filename.endswith('.txt'):
            table_name = os.path.splitext(filename)[0]
            file_path = os.path.join(CSV_FILES_DIR, filename)
            print(f"\nTraitement du fichier : {filename} -> Table : {table_name}")

            # Lire l'en-tête du fichier pour créer le modèle
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=CSV_DELIMITER)
                try:
                    header = next(reader)
                    model = create_gtfs_model(table_name, header)
                    # Ajouter le modèle dynamiquement à l'environnement global pour que SQLAlchemy le connaisse
                    globals()[model.__name__] = model
                except StopIteration:
                    print(f"  -> Le fichier '{filename}' est vide.")
                    continue
                except Exception as e:
                    print(f"  -> Erreur lors de la lecture de l'en-tête de '{filename}': {e}")
                    continue

            parsed_data = load_csv_file_to_dict(file_path)
            if parsed_data:
                db = SessionLocal()
                rows_from_file = insert_data(db, model, parsed_data, filename)
                total_rows_successfully_inserted += rows_from_file
                db.close()
            else:
                print(f"  -> Aucune donnée valide trouvée dans le fichier '{filename}'.")

    print(f"\n--- Processus de chargement dynamique terminé ---")
    print(f"Total de lignes insérées avec succès : {total_rows_successfully_inserted}")