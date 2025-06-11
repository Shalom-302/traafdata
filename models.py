# traafdata/models.py (avec corrections pour Trip et Shape)

from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

Base = declarative_base()

# --- GTFS Models ---

class Agency(Base):
    __tablename__ = 'agencies'
    agency_id = Column(String, primary_key=True, index=True)
    agency_name = Column(String, nullable=False)
    agency_url = Column(String, nullable=False)
    agency_timezone = Column(String, nullable=False)
    agency_lang = Column(String)
    agency_phone = Column(String)
    agency_fare_url = Column(String)
    agency_email = Column(String)

    routes = relationship("Route", back_populates="agency")


class Calendar(Base):
    __tablename__ = 'calendar'
    service_id = Column(String, primary_key=True, index=True)
    monday = Column(Integer, nullable=False)
    tuesday = Column(Integer, nullable=False)
    wednesday = Column(Integer, nullable=False)
    thursday = Column(Integer, nullable=False)
    friday = Column(Integer, nullable=False)
    saturday = Column(Integer, nullable=False)
    sunday = Column(Integer, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)

    trips = relationship("Trip", back_populates="calendar_service")
    calendar_dates = relationship("CalendarDate", back_populates="calendar_service")


class CalendarDate(Base):
    __tablename__ = 'calendar_dates'
    id = Column(Integer, primary_key=True, autoincrement=True)
    service_id = Column(String, ForeignKey('calendar.service_id'), nullable=False, index=True)
    date = Column(String, nullable=False)
    exception_type = Column(Integer, nullable=False)

    calendar_service = relationship("Calendar", back_populates="calendar_dates")


class FareAttribute(Base):
    __tablename__ = 'fare_attributes'
    fare_id = Column(String, primary_key=True, index=True)
    price = Column(Float, nullable=False)
    currency_type = Column(String, nullable=False)
    payment_method = Column(Integer, nullable=False)
    transfers = Column(Integer)
    agency_id = Column(String, ForeignKey('agencies.agency_id'))
    transfer_duration = Column(Integer)

    agency = relationship("Agency", backref="fare_attributes") # Using backref for simplicity if Agency doesn't define it
    fare_rules = relationship("FareRule", back_populates="fare_attribute")


class FareRule(Base):
    __tablename__ = 'fare_rules'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fare_id = Column(String, ForeignKey('fare_attributes.fare_id'), nullable=False, index=True)
    route_id = Column(String, ForeignKey('routes.route_id'))
    origin_id = Column(String, ForeignKey('stops.stop_id'))
    destination_id = Column(String, ForeignKey('stops.stop_id'))
    contains_id = Column(String, ForeignKey('stops.stop_id'))

    fare_attribute = relationship("FareAttribute", back_populates="fare_rules")
    route = relationship("Route", backref="fare_rules") # Using backref
    origin_stop = relationship("Stop", foreign_keys=[origin_id])
    destination_stop = relationship("Stop", foreign_keys=[destination_id])
    contains_stop = relationship("Stop", foreign_keys=[contains_id])


class FeedInfo(Base):
    __tablename__ = 'feed_info'
    feed_publisher_name = Column(String, primary_key=True, index=True)
    feed_publisher_url = Column(String, nullable=False)
    feed_lang = Column(String, nullable=False)
    default_lang = Column(String)
    feed_start_date = Column(String)
    feed_end_date = Column(String)
    feed_version = Column(String)
    feed_contact_email = Column(String)
    feed_contact_url = Column(String)


class Frequency(Base):
    __tablename__ = 'frequencies'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String, ForeignKey('trips.trip_id'), nullable=False, index=True)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    headway_secs = Column(Integer, nullable=False)
    exact_times = Column(Integer)

    trip = relationship("Trip", back_populates="frequencies")


class Level(Base):
    __tablename__ = 'levels'
    level_id = Column(String, primary_key=True, index=True)
    level_index = Column(Float, nullable=False)
    level_name = Column(String)


class Pathway(Base):
    __tablename__ = 'pathways'
    pathway_id = Column(String, primary_key=True, index=True)
    from_stop_id = Column(String, ForeignKey('stops.stop_id'), nullable=False)
    to_stop_id = Column(String, ForeignKey('stops.stop_id'), nullable=False)
    pathway_mode = Column(Integer, nullable=False)
    is_bidirectional = Column(Integer, nullable=False)
    length = Column(Float)
    traversal_time = Column(Integer)
    stair_count = Column(Integer)
    max_slope = Column(Float)
    min_width = Column(Float)
    signposted_as = Column(String)
    reversed_signposted_as = Column(String)

    from_stop = relationship("Stop", foreign_keys=[from_stop_id], back_populates="pathways_from")
    to_stop = relationship("Stop", foreign_keys=[to_stop_id], back_populates="pathways_to")


class Route(Base):
    __tablename__ = 'routes'
    route_id = Column(String, primary_key=True, index=True)
    agency_id = Column(String, ForeignKey('agencies.agency_id'))
    route_short_name = Column(String)
    route_long_name = Column(String)
    route_desc = Column(String)
    route_type = Column(Integer, nullable=False)
    route_url = Column(String)
    route_color = Column(String)
    route_text_color = Column(String)
    route_sort_order = Column(Integer)
    continuous_pickup = Column(Integer)
    continuous_drop_off = Column(Integer)

    agency = relationship("Agency", back_populates="routes")
    trips = relationship("Trip", back_populates="route")


class Shape(Base):
    __tablename__ = 'shapes'
    # id = Column(Integer, primary_key=True, autoincrement=True) # PK artificielle optionnelle
    shape_id = Column(String, nullable=False, index=True)
    shape_pt_lat = Column(Float, nullable=False)
    shape_pt_lon = Column(Float, nullable=False)
    shape_pt_sequence = Column(Integer, nullable=False)
    shape_dist_traveled = Column(Float)

    # La clé primaire est la combinaison de shape_id et shape_pt_sequence
    __table_args__ = (
        PrimaryKeyConstraint('shape_id', 'shape_pt_sequence', name='pk_shapes'),
        # UniqueConstraint('shape_id', 'shape_pt_sequence', name='_shape_point_uc'), # Redondant si PK
    )
    # La relation 'trips' n'a pas de sens ici si elle est basée sur une FK de Trip vers Shape.
    # Si un Shape (point) appartenait à plusieurs trips, ce serait différent, mais ce n'est pas le cas.
    # trips = relationship("Trip", back_populates="shape_point") # A REVOIR/SUPPRIMER


class StopTime(Base):
    __tablename__ = 'stop_times'
    id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(String, ForeignKey('trips.trip_id'), nullable=False, index=True)
    arrival_time = Column(String)
    departure_time = Column(String)
    stop_id = Column(String, ForeignKey('stops.stop_id'), nullable=False, index=True)
    stop_sequence = Column(Integer, nullable=False)
    stop_headsign = Column(String)
    pickup_type = Column(Integer)
    drop_off_type = Column(Integer)
    shape_dist_traveled = Column(Float)
    timepoint = Column(Integer)
    fare_units_traveled = Column(Integer)
    continuous_pickup = Column(Integer)
    continuous_drop_off = Column(Integer)

    trip = relationship("Trip", back_populates="stop_times")
    stop = relationship("Stop", back_populates="stop_times")


class Stop(Base):
    __tablename__ = 'stops'
    stop_id = Column(String, primary_key=True, index=True)
    stop_code = Column(String)
    stop_name = Column(String)
    stop_desc = Column(String)
    stop_lat = Column(Float)
    stop_lon = Column(Float)
    zone_id = Column(String)
    stop_url = Column(String)
    location_type = Column(Integer)
    parent_station = Column(String, ForeignKey('stops.stop_id'))
    stop_timezone = Column(String)
    wheelchair_boarding = Column(Integer)
    level_id = Column(String, ForeignKey('levels.level_id'))
    platform_code = Column(String)

    parent = relationship("Stop", remote_side=[stop_id], backref="children_stops") # Added backref for clarity
    level = relationship("Level", backref="stops") # Using backref

    stop_times = relationship("StopTime", back_populates="stop")
    pathways_from = relationship("Pathway", foreign_keys=[Pathway.from_stop_id], back_populates="from_stop")
    pathways_to = relationship("Pathway", foreign_keys=[Pathway.to_stop_id], back_populates="to_stop")


class Transfer(Base):
    __tablename__ = 'transfers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_stop_id = Column(String, ForeignKey('stops.stop_id'), nullable=False)
    to_stop_id = Column(String, ForeignKey('stops.stop_id'), nullable=False)
    transfer_type = Column(Integer, nullable=False)
    min_transfer_time = Column(Integer)

    from_stop = relationship("Stop", foreign_keys=[from_stop_id], backref="transfers_from")
    to_stop = relationship("Stop", foreign_keys=[to_stop_id], backref="transfers_to")


class Trip(Base):
    __tablename__ = 'trips'
    trip_id = Column(String, primary_key=True, index=True)
    route_id = Column(String, ForeignKey('routes.route_id'), nullable=False, index=True)
    service_id = Column(String, ForeignKey('calendar.service_id'), nullable=False, index=True)
    
    # shape_id est juste un identifiant (String). Pas de contrainte de clé étrangère ici.
    # La liaison se fait par convention : vous interrogerez la table 'shapes'
    # en utilisant la valeur de 'trips.shape_id'.
    shape_id = Column(String, index=True) # <--- CORRECTION IMPORTANTE
    
    trip_headsign = Column(String)
    trip_short_name = Column(String)
    direction_id = Column(Integer)
    block_id = Column(String)
    wheelchair_accessible = Column(Integer)
    bikes_allowed = Column(Integer)

    route = relationship("Route", back_populates="trips")
    calendar_service = relationship("Calendar", back_populates="trips")
    
    # La relation 'shape_point' (ou similaire) n'est pas définie par une FK ici.
    # Si vous voulez accéder aux points de forme pour un trip, vous le ferez via une requête:
    # e.g., session.query(Shape).filter(Shape.shape_id == trip_instance.shape_id).order_by(Shape.shape_pt_sequence)
    # Par conséquent, la relation directe 'shape_point = relationship("Shape", ...)'
    # n'est pas appropriée ici telle qu'elle était définie, car elle impliquait une FK.
    # Je la supprime pour éviter la confusion. Si vous avez besoin d'une méthode pratique,
    # vous pouvez ajouter une propriété Python à votre classe Trip.

    stop_times = relationship("StopTime", back_populates="trip")
    frequencies = relationship("Frequency", back_populates="trip")