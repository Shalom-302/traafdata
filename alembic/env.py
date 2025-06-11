from logging.config import fileConfig
import os
from dotenv import load_dotenv # <--- AJOUTEZ CET IMPORT

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Charger les variables d'environnement depuis le fichier .env
# Assurez-vous que votre fichier .env est à la racine du projet
# ou à un endroit où load_dotenv() peut le trouver.
# Par défaut, il cherche un fichier .env dans le répertoire courant
# ou les répertoires parents.
load_dotenv() # <--- APPELEZ load_dotenv() ICI

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata

# Importez votre/vos fichiers de modèles SQLAlchemy
from models import Base  # Assurez-vous que le chemin est correct !
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.
    """
    # Pour le mode offline, nous devrions aussi utiliser les variables d'env
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT", "5432") # Ajoutez le port si nécessaire

    if not all([db_host, db_name, db_user, db_password]):
        # Vous pouvez choisir de lever une erreur ou d'utiliser une URL par défaut
        # issue de alembic.ini si vous le souhaitez pour le mode offline.
        # Pour l'instant, utilisons l'URL de alembic.ini si les vars d'env ne sont pas là.
        url = config.get_main_option("sqlalchemy.url")
        if not url: # Si sqlalchemy.url n'est pas non plus dans alembic.ini
             raise ValueError(
                "Les variables d'environnement DB_* ou sqlalchemy.url dans alembic.ini doivent être définies pour le mode offline."
            )
    else:
        url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.
    """
    # Récupérez l'URL de la base de données depuis les variables d'environnement
    # os.environ.get() lira maintenant les variables chargées par load_dotenv()
    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_port = os.environ.get("DB_PORT", "5432") # Ajoutez le port si nécessaire

    if not all([db_host, db_name, db_user, db_password]):
        raise ValueError(
            "Les variables d'environnement DB_HOST, DB_NAME, DB_USER et DB_PASSWORD doivent être définies."
        )

    sqlalchemy_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

    # Il est préférable de créer un nouveau moteur avec l'URL construite
    # plutôt que de surcharger l'URL d'un moteur créé à partir de config.
    # connectable = engine_from_config(
    #     config.get_section(config.config_ini_section, {}), # Ceci lit sqlalchemy.url de alembic.ini
    #     prefix="sqlalchemy.",
    #     poolclass=pool.NullPool,
    # )
    # connectable.url = sqlalchemy_url  # Surchargez l'URL avec celle construite

    # Créez une configuration pour engine_from_config dynamiquement
    # en utilisant l'URL que nous venons de construire.
    engine_config = config.get_section(config.config_ini_section, {})
    engine_config['sqlalchemy.url'] = sqlalchemy_url

    connectable = engine_from_config(
        engine_config,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()