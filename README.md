# API Données GTFS Traaf

Une API pour accéder aux données GTFS stockées dans PostgreSQL.

## Features

- **GTFS Data Loading:** Loads GTFS data from standard text files (e.g., `stops.txt`, `routes.txt`) into a PostgreSQL database.
- **Relational Database Storage:** Utilizes a PostgreSQL database to store and manage GTFS data, enabling complex queries and relationships.
- **Database Migrations:** Employs Alembic to manage database schema migrations, ensuring schema consistency across different environments.
- **RESTful API:** Provides a FastAPI-based API to access and query the GTFS data.
- **Data Validation:** Uses Pydantic schemas for robust data validation in API requests and responses.
- **Dynamic Table Creation:** The `loadata.py` script can dynamically create database tables based on the headers of the GTFS text files.

## Core Technologies Used

- **FastAPI:** For building the high-performance RESTful API.
- **SQLAlchemy:** As the ORM for interacting with the PostgreSQL database.
- **Alembic:** For managing database schema migrations.
- **Pydantic:** For data validation and settings management.
- **PostgreSQL:** As the relational database for storing GTFS data.
- **Python:** The programming language used for the project.

## Project Structure

```
.
├── alembic/              # Alembic migration scripts
├── data/                 # GTFS data files (e.g., stops.txt, routes.txt)
├── .gitignore            # Specifies intentionally untracked files that Git should ignore
├── __init__.py           # Makes Python treat the directory as a package
├── alembic.ini           # Alembic configuration file
├── crud.py               # Contains CRUD (Create, Read, Update, Delete) database operations
├── db.py                 # Database session management and engine configuration
├── loadata.py            # Script to load GTFS data from .txt files into the database
├── main.py               # FastAPI application entry point, defines API endpoints
├── models.py             # SQLAlchemy ORM models representing database tables
├── README.md             # This file
├── requirements.txt      # Project dependencies
├── schemas.py            # Pydantic schemas for data validation and serialization
└── seed.py               # Script for seeding initial data (if applicable, may overlap with loadata.py)
```

- **`main.py`**: The main entry point for the FastAPI application. Defines API endpoints and application settings.
- **`db.py`**: Handles database connection setup and session management for SQLAlchemy.
- **`models.py`**: Defines the SQLAlchemy ORM models that map to database tables.
- **`schemas.py`**: Contains Pydantic schemas used for API request/response validation and data serialization.
- **`crud.py`**: Implements reusable functions for common database operations (Create, Read, Update, Delete).
- **`loadata.py`**: Script responsible for parsing GTFS text files from the `data/` directory and loading them into the database.
- **`alembic/`**: Directory containing Alembic migration scripts for managing database schema changes.
- **`alembic.ini`**: Configuration file for Alembic.
- **`data/`**: Directory where raw GTFS data files (typically `.txt`) should be placed.
- **`requirements.txt`**: Lists all Python dependencies required for the project.
- **`seed.py`**: A script that might be used for populating the database with initial or specific data sets. Its role might be similar to or complementary to `loadata.py`.

## Setup and Installation

Follow these steps to set up and run the project locally:

1.  **Clone the Repository:**
    ```bash
    git clone <repository_url> # Replace <repository_url> with the actual URL
    cd <repository_directory_name>
    ```

2.  **Create and Activate a Virtual Environment:**
    It's recommended to use a virtual environment to manage project dependencies.
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    Install all required packages listed in `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up PostgreSQL Database:**
    Ensure you have PostgreSQL installed and running. Create a new database for this project.
    For example, using `psql`:
    ```sql
    CREATE DATABASE gtfs_db;
    ```
    You will also need a database user with permissions to access this database.

5.  **Configure Database Connection:**
    The database connection is configured in `db.py`. You might need to adjust the `DATABASE_URL` based on your PostgreSQL setup (username, password, host, port, database name).
    It's common to use environment variables for sensitive information. For example, `db.py` might look for:
    ```python
    # Example from a typical db.py structure
    # from sqlalchemy import create_engine
    # from sqlalchemy.ext.declarative import declarative_base
    # from sqlalchemy.orm import sessionmaker
    # import os

    # DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@host:port/dbname")
    # engine = create_engine(DATABASE_URL)
    # SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    # Base = declarative_base()
    ```
    Ensure the environment variable `DATABASE_URL` is set or update the connection string directly if needed.
    A typical `DATABASE_URL` format is `postgresql://username:password@host:port/database_name`.

6.  **Run Database Migrations:**
    Alembic is used to manage database schema. Apply the migrations to create the necessary tables:
    ```bash
    alembic upgrade head
    ```
    This command reads the migration scripts in the `alembic/versions/` directory and applies them to your database.

7.  **Load GTFS Data:**
    Place your GTFS data files (e.g., `agency.txt`, `stops.txt`, etc.) into the `data/` directory.
    Then, run the `loadata.py` script to populate the database:
    ```bash
    python loadata.py
    ```
    This script will read the `.txt` files, dynamically create tables if they don't exist (though Alembic should handle table creation), and insert the data.

## Running the Application

Once the setup is complete, you can run the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

-   `main:app`: Refers to the `app` instance created in the `main.py` file.
-   `--reload`: Enables auto-reloading, so the server will restart automatically when code changes are detected (useful for development).

After starting the server, you can access the API in your browser or through an API client:

-   **API Base URL:** `http://127.0.0.1:8000`
-   **Interactive API Documentation (Swagger UI):** `http://127.0.0.1:8000/docs`
-   **Alternative API Documentation (ReDoc):** `http://127.0.0.1:8000/redoc`

The interactive documentation allows you to explore and test the API endpoints directly from your browser.

## API Endpoints

The API provides several endpoints to access GTFS data. Below are some of the main resources available. For a complete list of endpoints, request/response models, and testing capabilities, please refer to the interactive API documentation at `/docs`.

-   **Agencies:**
    -   `GET /agencies/`: Retrieve a list of transit agencies.
    -   `GET /agencies/{agency_id}`: Retrieve a specific agency by its ID.
-   **Stops:**
    -   `GET /stops/`: Retrieve a list of stops.
    -   `GET /stops/{stop_id}`: Retrieve a specific stop by its ID.
-   **Routes:**
    -   `GET /routes/`: Retrieve a list of routes. Can be filtered by `agency_id`.
    -   `GET /routes/{route_id}`: Retrieve a specific route by its ID.
-   **Trips:**
    -   `GET /routes/{route_id}/trips/`: Retrieve trips for a specific route.
    -   `GET /trips/{trip_id}`: Retrieve a specific trip by its ID.
-   **Stop Times:**
    -   `GET /trips/{trip_id}/stop_times/`: Retrieve stop times for a specific trip.

Additional endpoints for other GTFS entities (like Calendar, Calendar Dates, Shapes, etc.) may be available or can be added. Check the `/docs` for the most current information.

## Data Loading

The GTFS data is loaded into the PostgreSQL database from text files located in the `data/` directory. The script responsible for this process is `loadata.py`.

**Process:**

1.  **Place GTFS Files:** Ensure your GTFS `.txt` files (e.g., `agency.txt`, `stops.txt`, `routes.txt`, `trips.txt`, `stop_times.txt`, etc.) are present in the `data/` directory.
2.  **Run the Script:** Execute the `loadata.py` script from the root of the project:
    ```bash
    python loadata.py
    ```
3.  **Dynamic Table Handling:** The script is designed to read the header row of each GTFS file to determine the table structure. It can dynamically create SQLAlchemy models and corresponding database tables if they do not already exist (though table creation is primarily managed by Alembic migrations).
4.  **Data Insertion:** Data from each row in the text files is then inserted into the appropriate database table. The script handles potential duplicate entries by skipping them if an `IntegrityError` occurs.

If you update the GTFS files in the `data/` directory, you may need to re-run `loadata.py` to reflect these changes in the database. Depending on the desired behavior for existing data, you might need to clear tables before reloading or implement more sophisticated update logic.
