# main.py

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

# Supposons que crud.py, models.py, schemas.py, db.py sont au même niveau que main.py
# ou que main.py est dans un package et les autres sont des modules de ce package.
import crud
import models
import schemas
from db import get_db # Importer uniquement la dépendance get_db

#
# LA LIGNE SUIVANTE DOIT ÊTRE SUPPRIMÉE OU COMMENTÉE
# C'est Alembic qui gère la création/mise à jour des tables.
# models.Base.metadata.create_all(bind=engine) # <--- SUPPRIMER/COMMENTER CECI
#

app = FastAPI(
    title="API Données GTFS Traaf",
    description="Une API pour accéder aux données GTFS stockées dans PostgreSQL.",
    version="0.1.0",
)

# --- Routes pour Agency ---
@app.get("/agencies/", response_model=List[schemas.Agency], tags=["Agencies"])
def read_agencies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère une liste d'agences.
    """
    agencies = crud.get_agencies(db, skip=skip, limit=limit)
    return agencies

@app.get("/agencies/{agency_id}", response_model=schemas.Agency, tags=["Agencies"])
def read_agency(agency_id: str, db: Session = Depends(get_db)):
    """
    Récupère une agence spécifique par son ID.
    """
    db_agency = crud.get_agency(db, agency_id=agency_id)
    if db_agency is None:
        raise HTTPException(status_code=404, detail="Agency not found")
    return db_agency

# --- Routes pour Stop ---
@app.get("/stops/", response_model=List[schemas.Stop], tags=["Stops"])
def read_stops(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère une liste d'arrêts.
    """
    stops = crud.get_stops(db, skip=skip, limit=limit)
    return stops
    
@app.get("/stops/{stop_id}", response_model=schemas.Stop, tags=["Stops"])
def read_stop(stop_id: str, db: Session = Depends(get_db)):
    """
    Récupère un arrêt spécifique par son ID.
    """
    db_stop = crud.get_stop(db, stop_id=stop_id)
    if db_stop is None:
        raise HTTPException(status_code=404, detail="Stop not found")
    return db_stop

# --- Routes pour Route ---
@app.get("/routes/", response_model=List[schemas.Route], tags=["Routes"])
def read_routes(agency_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère une liste de routes, avec un filtre optionnel par agency_id.
    """
    routes = crud.get_routes(db, agency_id=agency_id, skip=skip, limit=limit)
    return routes

@app.get("/routes/{route_id}", response_model=schemas.Route, tags=["Routes"])
def read_route(route_id: str, db: Session = Depends(get_db)):
    """
    Récupère une route spécifique par son ID.
    """
    db_route = crud.get_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route


# --- Routes pour Trip ---
@app.get("/routes/{route_id}/trips/", response_model=List[schemas.Trip], tags=["Trips"])
def read_trips_for_route(route_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère les trajets pour une route spécifique.
    """
    db_route = crud.get_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    trips = crud.get_trips_by_route(db, route_id=route_id, skip=skip, limit=limit)
    return trips

@app.get("/trips/{trip_id}", response_model=schemas.Trip, tags=["Trips"])
def read_trip(trip_id: str, db: Session = Depends(get_db)):
    """
    Récupère un trajet spécifique par son ID.
    """
    db_trip = crud.get_trip(db, trip_id=trip_id) # Vous devrez ajouter get_trip à crud.py
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# --- Routes pour StopTime ---
@app.get("/trips/{trip_id}/stop_times/", response_model=List[schemas.StopTime], tags=["StopTimes"])
def read_stop_times_for_trip(trip_id: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Récupère les horaires d'arrêt pour un trajet spécifique.
    """
    db_trip = crud.get_trip(db, trip_id=trip_id) # Vérifier si le trajet existe
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    stop_times = crud.get_stop_times_by_trip(db, trip_id=trip_id, skip=skip, limit=limit)
    # if not stop_times: # Cette vérification est redondante si le trip existe
    #     pass
    return stop_times
    
# TODO: Ajoutez des routes pour les autres entités GTFS (Calendar, CalendarDate, Shapes, Frequencies, etc.)
# en suivant le même modèle :
# 1. Définir la route avec @app.get(...)
# 2. Spécifier le response_model avec votre schéma Pydantic
# 3. Ajouter une fonction CRUD correspondante dans crud.py
# 4. Appeler la fonction CRUD et retourner le résultat.

# Exemple de route pour Calendar (à compléter dans crud.py et schemas.py)
# @app.get("/calendar/{service_id}", response_model=schemas.Calendar, tags=["Calendar"])
# def read_calendar_service(service_id: str, db: Session = Depends(get_db)):
#     db_calendar = crud.get_calendar_service(db, service_id=service_id)
#     if db_calendar is None:
#         raise HTTPException(status_code=404, detail="Calendar service not found")
#     return db_calendar

# N'oubliez pas d'appeler MonSchema.update_forward_refs() à la fin de votre fichier schemas.py
# si vous utilisez des références forward pour les relations dans vos schémas Pydantic.
# Par exemple, si schemas.Route contient une référence à schemas.Agency et vice-versa.
# (cela se fait dans schemas.py, pas ici)