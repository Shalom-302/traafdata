from pydantic import BaseModel
from typing import Optional, List

# Schéma pour Agency (déjà existant, mais inclus pour complétude)
class AgencyBase(BaseModel):
    agency_id: str
    agency_name: str
    agency_url: str
    agency_timezone: str
    agency_lang: Optional[str] = None
    agency_phone: Optional[str] = None
    agency_fare_url: Optional[str] = None
    agency_email: Optional[str] = None

class Agency(AgencyBase):
    class Config:
        from_attributes = True # Anciennement orm_mode = True

# Nouveaux Schémas basés sur les modèles GTFS

class CalendarBase(BaseModel):
    service_id: str
    monday: int
    tuesday: int
    wednesday: int
    thursday: int
    friday: int
    saturday: int
    sunday: int
    start_date: str
    end_date: str

class Calendar(CalendarBase):
    class Config:
        from_attributes = True

class CalendarDateBase(BaseModel):
    service_id: str
    date: str
    exception_type: int

class CalendarDate(CalendarDateBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class FareAttributeBase(BaseModel):
    fare_id: str
    price: float
    currency_type: str
    payment_method: int
    transfers: Optional[int] = None
    agency_id: Optional[str] = None # Réfère à agency_id
    transfer_duration: Optional[int] = None

class FareAttribute(FareAttributeBase):
    class Config:
        from_attributes = True

class FareRuleBase(BaseModel):
    fare_id: str # Réfère à fare_id
    route_id: Optional[str] = None # Réfère à route_id
    origin_id: Optional[str] = None
    destination_id: Optional[str] = None
    contains_id: Optional[str] = None

class FareRule(FareRuleBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class FeedInfoBase(BaseModel):
    feed_publisher_name: str
    feed_publisher_url: str
    feed_lang: str
    default_lang: Optional[str] = None
    feed_start_date: Optional[str] = None
    feed_end_date: Optional[str] = None
    feed_version: Optional[str] = None
    feed_contact_email: Optional[str] = None
    feed_contact_url: Optional[str] = None

class FeedInfo(FeedInfoBase):
    class Config:
        from_attributes = True

class FrequencyBase(BaseModel):
    trip_id: str # Réfère à trip_id
    start_time: str # Format HH:MM:SS
    end_time: str # Format HH:MM:SS
    headway_secs: int
    exact_times: Optional[int] = None

class Frequency(FrequencyBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class LevelBase(BaseModel):
    level_id: str
    level_index: float
    level_name: Optional[str] = None

class Level(LevelBase):
    class Config:
        from_attributes = True

class PathwayBase(BaseModel):
    pathway_id: str
    from_stop_id: str # Réfère à stop_id
    to_stop_id: str # Réfère à stop_id
    pathway_mode: int
    is_bidirectional: int
    length: Optional[float] = None
    traversal_time: Optional[int] = None
    stair_count: Optional[int] = None
    max_slope: Optional[float] = None
    min_width: Optional[float] = None
    signposted_as: Optional[str] = None
    reversed_signposted_as: Optional[str] = None

class Pathway(PathwayBase):
    class Config:
        from_attributes = True

class RouteBase(BaseModel):
    route_id: str
    agency_id: Optional[str] = None # Réfère à agency_id
    route_short_name: Optional[str] = None
    route_long_name: Optional[str] = None
    route_desc: Optional[str] = None
    route_type: int
    route_url: Optional[str] = None
    route_color: Optional[str] = None
    route_text_color: Optional[str] = None
    route_sort_order: Optional[int] = None
    continuous_pickup: Optional[int] = None
    continuous_drop_off: Optional[int] = None

class Route(RouteBase):
    class Config:
        from_attributes = True

class ShapeBase(BaseModel):
    shape_id: str
    shape_pt_lat: float
    shape_pt_lon: float
    shape_pt_sequence: int
    shape_dist_traveled: Optional[float] = None

class Shape(ShapeBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class StopTimeBase(BaseModel):
    trip_id: str # Réfère à trip_id
    arrival_time: str # Format HH:MM:SS
    departure_time: str # Format HH:MM:SS
    stop_id: str # Réfère à stop_id
    stop_sequence: int
    stop_headsign: Optional[str] = None
    pickup_type: Optional[int] = None
    drop_off_type: Optional[int] = None
    continuous_pickup: Optional[int] = None
    continuous_drop_off: Optional[int] = None
    timepoint: Optional[int] = None

class StopTime(StopTimeBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class StopBase(BaseModel):
    stop_id: str
    stop_code: Optional[str] = None
    stop_name: str
    stop_desc: Optional[str] = None
    stop_lat: float
    stop_lon: float
    zone_id: Optional[str] = None
    stop_url: Optional[str] = None
    location_type: Optional[int] = None
    parent_station: Optional[str] = None # Réfère à stop_id (self-referencing)
    stop_timezone: Optional[str] = None
    wheelchair_boarding: Optional[int] = None
    platform_code: Optional[str] = None

class Stop(StopBase):
    class Config:
        from_attributes = True

class TransferBase(BaseModel):
    from_stop_id: str # Réfère à stop_id
    to_stop_id: str # Réfère à stop_id
    transfer_type: int
    min_transfer_time: Optional[int] = None

class Transfer(TransferBase):
    id: int # Ajouté car c'est une PK artificielle
    class Config:
        from_attributes = True

class TripBase(BaseModel):
    trip_id: str
    route_id: str # Réfère à route_id
    service_id: str # Réfère à service_id
    shape_id: Optional[str] = None # Réfère à shape_id
    trip_headsign: Optional[str] = None
    trip_short_name: Optional[str] = None
    direction_id: Optional[int] = None
    block_id: Optional[str] = None
    wheelchair_accessible: Optional[int] = None
    bikes_allowed: Optional[int] = None

class Trip(TripBase):
    class Config:
        from_attributes = True