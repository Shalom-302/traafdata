# app/crud.py
from sqlalchemy.orm import Session
import models, schemas # Ajustez les imports
from typing import List, Optional

# --- Agency CRUD ---
def get_agency(db: Session, agency_id: str) -> Optional[models.Agency]:
    return db.query(models.Agency).filter(models.Agency.agency_id == agency_id).first()

def get_agencies(db: Session, skip: int = 0, limit: int = 100) -> List[models.Agency]:
    return db.query(models.Agency).offset(skip).limit(limit).all()

# Pour GTFS, la création se fait via le seed. Mais si vous voulez ajouter un CRUD :
# def create_agency(db: Session, agency: schemas.AgencyCreate) -> models.Agency:
#     db_agency = models.Agency(**agency.dict())
#     db.add(db_agency)
#     db.commit()
#     db.refresh(db_agency)
#     return db_agency

# --- Stop CRUD ---
def get_stop(db: Session, stop_id: str) -> Optional[models.Stop]:
    return db.query(models.Stop).filter(models.Stop.stop_id == stop_id).first()

def get_stops(db: Session, skip: int = 0, limit: int = 100) -> List[models.Stop]:
    return db.query(models.Stop).offset(skip).limit(limit).all()

# --- Route CRUD ---
def get_route(db: Session, route_id: str) -> Optional[models.Route]:
    return db.query(models.Route).filter(models.Route.route_id == route_id).first()

def get_routes(db: Session, agency_id: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[models.Route]:
    query = db.query(models.Route)
    if agency_id:
        query = query.filter(models.Route.agency_id == agency_id)
    return query.offset(skip).limit(limit).all()

# --- Trip CRUD ---
def get_trips_by_route(db: Session, route_id: str, skip: int = 0, limit: int = 100) -> List[models.Trip]:
    return db.query(models.Trip).filter(models.Trip.route_id == route_id).offset(skip).limit(limit).all()

# --- StopTime CRUD ---
def get_stop_times_by_trip(db: Session, trip_id: str, skip: int = 0, limit: int = 100) -> List[models.StopTime]:
    return db.query(models.StopTime).filter(models.StopTime.trip_id == trip_id).order_by(models.StopTime.stop_sequence).offset(skip).limit(limit).all()

# Ajoutez des fonctions CRUD pour tous vos autres modèles...
# Ex: get_calendar_by_service_id, get_shapes_for_trip_id, etc.