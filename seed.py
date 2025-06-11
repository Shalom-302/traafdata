import csv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Importer vos modèles SQLAlchemy
from models import Base, Agency, Stop, Route, Trip, StopTime, Calendar, CalendarDate, FeedInfo, Shape, Frequency, Level, Pathway, FareAttribute, FareRule, Transfer

load_dotenv()

# --- Configuration de la base de données ---
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "agency_db")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Chemin vers le dossier des données GTFS ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

# --- Fonctions d'aide pour la conversion de type et les valeurs par défaut ---
def to_int(value, default=None):
    if value is None or value == '':
        return default
    try:
        return int(value)
    except ValueError:
        return default

def to_float(value, default=None):
    if value is None or value == '':
        return default
    try:
        return float(value)
    except ValueError:
        return default

def to_str(value, default=None):
    if value is None or value == '':
        return default
    return str(value)

# --- Fonctions de seeding pour chaque fichier GTFS ---

def seed_agencies(db_session):
    filepath = os.path.join(DATA_DIR, 'agency.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding agencies...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            agency = Agency(
                agency_id=to_str(row.get('agency_id')),
                agency_name=to_str(row.get('agency_name')),
                agency_url=to_str(row.get('agency_url')),
                agency_timezone=to_str(row.get('agency_timezone')),
                agency_lang=to_str(row.get('agency_lang')),
                agency_phone=to_str(row.get('agency_phone')),
                agency_fare_url=to_str(row.get('agency_fare_url')),
                agency_email=to_str(row.get('agency_email'))
            )
            db_session.add(agency)
    db_session.commit()
    print("Agencies seeded.")

def seed_stops(db_session):
    filepath = os.path.join(DATA_DIR, 'stops.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding stops...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            stop = Stop(
                stop_id=to_str(row.get('stop_id')),
                stop_code=to_str(row.get('stop_code')),
                stop_name=to_str(row.get('stop_name')),
                stop_desc=to_str(row.get('stop_desc')),
                stop_lat=to_float(row.get('stop_lat')),
                stop_lon=to_float(row.get('stop_lon')),
                zone_id=to_str(row.get('zone_id')),
                stop_url=to_str(row.get('stop_url')),
                location_type=to_int(row.get('location_type')),
                parent_station=to_str(row.get('parent_station')) if row.get('parent_station') else None,
                stop_timezone=to_str(row.get('stop_timezone')),
                wheelchair_boarding=to_int(row.get('wheelchair_boarding')),
                level_id=to_str(row.get('level_id')) if row.get('level_id') else None,
                platform_code=to_str(row.get('platform_code'))
            )
            db_session.add(stop)
    db_session.commit()
    print("Stops seeded.")

def seed_routes(db_session):
    filepath = os.path.join(DATA_DIR, 'routes.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding routes...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            route = Route(
                route_id=to_str(row.get('route_id')),
                agency_id=to_str(row.get('agency_id')) if row.get('agency_id') else None,
                route_short_name=to_str(row.get('route_short_name')),
                route_long_name=to_str(row.get('route_long_name')),
                route_desc=to_str(row.get('route_desc')),
                route_type=to_int(row.get('route_type')),
                route_url=to_str(row.get('route_url')),
                route_color=to_str(row.get('route_color')),
                route_text_color=to_str(row.get('route_text_color')),
                route_sort_order=to_int(row.get('route_sort_order')),
                continuous_pickup=to_int(row.get('continuous_pickup')),
                continuous_drop_off=to_int(row.get('continuous_drop_off'))
            )
            db_session.add(route)
    db_session.commit()
    print("Routes seeded.")

def seed_calendar(db_session):
    filepath = os.path.join(DATA_DIR, 'calendar.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding calendar...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calendar_entry = Calendar(
                service_id=to_str(row.get('service_id')),
                monday=to_int(row.get('monday')),
                tuesday=to_int(row.get('tuesday')),
                wednesday=to_int(row.get('wednesday')),
                thursday=to_int(row.get('thursday')),
                friday=to_int(row.get('friday')),
                saturday=to_int(row.get('saturday')),
                sunday=to_int(row.get('sunday')),
                start_date=to_str(row.get('start_date')),
                end_date=to_str(row.get('end_date'))
            )
            db_session.add(calendar_entry)
    db_session.commit()
    print("Calendar seeded.")

def seed_calendar_dates(db_session):
    filepath = os.path.join(DATA_DIR, 'calendar_dates.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding calendar_dates...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            calendar_date_entry = CalendarDate(
                service_id=to_str(row.get('service_id')),
                date=to_str(row.get('date')),
                exception_type=to_int(row.get('exception_type'))
            )
            db_session.add(calendar_date_entry)
    db_session.commit()
    print("Calendar dates seeded.")

def seed_shapes(db_session):
    filepath = os.path.join(DATA_DIR, 'shapes.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding shapes...")
    shapes_batch = []
    batch_size = 10000
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            shape_entry = Shape(
                shape_id=to_str(row.get('shape_id')),
                shape_pt_lat=to_float(row.get('shape_pt_lat')),
                shape_pt_lon=to_float(row.get('shape_pt_lon')),
                shape_pt_sequence=to_int(row.get('shape_pt_sequence')),
                shape_dist_traveled=to_float(row.get('shape_dist_traveled'), default=0.0)
            )
            shapes_batch.append(shape_entry)
            if (i + 1) % batch_size == 0:
                db_session.add_all(shapes_batch)
                db_session.commit()
                print(f"Committed {len(shapes_batch)} shapes.")
                shapes_batch = []
        
        if shapes_batch:
            db_session.add_all(shapes_batch)
            db_session.commit()
            print(f"Committed {len(shapes_batch)} shapes (final batch).")
    print("Shapes seeded.")

def seed_trips(db_session):
    filepath = os.path.join(DATA_DIR, 'trips.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding trips...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            trip = Trip(
                trip_id=to_str(row.get('trip_id')),
                route_id=to_str(row.get('route_id')),
                service_id=to_str(row.get('service_id')),
                shape_id=to_str(row.get('shape_id')) if row.get('shape_id') else None,
                trip_headsign=to_str(row.get('trip_headsign')),
                trip_short_name=to_str(row.get('trip_short_name')),
                direction_id=to_int(row.get('direction_id')),
                block_id=to_str(row.get('block_id')),
                wheelchair_accessible=to_int(row.get('wheelchair_accessible')),
                bikes_allowed=to_int(row.get('bikes_allowed'))
            )
            db_session.add(trip)
    db_session.commit()
    print("Trips seeded.")

def seed_stop_times(db_session):
    filepath = os.path.join(DATA_DIR, 'stop_times.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé.")
        return
    print("Seeding stop_times...")
    stop_times_batch = []
    batch_size = 10000
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            stop_time = StopTime(
                trip_id=to_str(row.get('trip_id')),
                arrival_time=to_str(row.get('arrival_time')),
                departure_time=to_str(row.get('departure_time')),
                stop_id=to_str(row.get('stop_id')),
                stop_sequence=to_int(row.get('stop_sequence')),
                stop_headsign=to_str(row.get('stop_headsign')),
                pickup_type=to_int(row.get('pickup_type'), default=0),
                drop_off_type=to_int(row.get('drop_off_type'), default=0),
                shape_dist_traveled=to_float(row.get('shape_dist_traveled')),
                timepoint=to_int(row.get('timepoint'))
            )
            stop_times_batch.append(stop_time)
            if (i + 1) % batch_size == 0:
                db_session.add_all(stop_times_batch)
                db_session.commit()
                print(f"Committed {len(stop_times_batch)} stop_times.")
                stop_times_batch = []
        
        if stop_times_batch:
            db_session.add_all(stop_times_batch)
            db_session.commit()
            print(f"Committed {len(stop_times_batch)} stop_times (final batch).")
    print("Stop_times seeded.")

# ***** DÉBUT DES FONCTIONS AJOUTÉES/CORRIGÉES *****
def seed_levels(db_session):
    filepath = os.path.join(DATA_DIR, 'levels.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping levels seeding.")
        return
    print("Seeding levels...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            level_entry = Level(
                level_id=to_str(row.get('level_id')),
                level_index=to_float(row.get('level_index')),
                level_name=to_str(row.get('level_name'))
            )
            db_session.add(level_entry)
    db_session.commit()
    print("Levels seeded.")

def seed_frequencies(db_session):
    filepath = os.path.join(DATA_DIR, 'frequencies.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping frequencies seeding.")
        return
    print("Seeding frequencies...")
    frequencies_batch = []
    batch_size = 5000
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            frequency_entry = Frequency(
                trip_id=to_str(row.get('trip_id')),
                start_time=to_str(row.get('start_time')),
                end_time=to_str(row.get('end_time')),
                headway_secs=to_int(row.get('headway_secs')),
                exact_times=to_int(row.get('exact_times'))
            )
            frequencies_batch.append(frequency_entry)
            if (i + 1) % batch_size == 0:
                db_session.add_all(frequencies_batch)
                db_session.commit()
                print(f"Committed {len(frequencies_batch)} frequencies.")
                frequencies_batch = []
        
        if frequencies_batch:
            db_session.add_all(frequencies_batch)
            db_session.commit()
            print(f"Committed {len(frequencies_batch)} frequencies (final batch).")
    print("Frequencies seeded.")

def seed_feed_info(db_session):
    filepath = os.path.join(DATA_DIR, 'feed_info.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping feed_info seeding.")
        return
    print("Seeding feed_info...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            feed_info_entry = FeedInfo(
                feed_publisher_name=to_str(row.get('feed_publisher_name')),
                feed_publisher_url=to_str(row.get('feed_publisher_url')),
                feed_lang=to_str(row.get('feed_lang')),
                default_lang=to_str(row.get('default_lang')),
                feed_start_date=to_str(row.get('feed_start_date')),
                feed_end_date=to_str(row.get('feed_end_date')),
                feed_version=to_str(row.get('feed_version')),
                feed_contact_email=to_str(row.get('feed_contact_email')),
                feed_contact_url=to_str(row.get('feed_contact_url'))
            )
            db_session.add(feed_info_entry)
    db_session.commit()
    print("Feed_info seeded.")

def seed_pathways(db_session):
    filepath = os.path.join(DATA_DIR, 'pathways.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping pathways seeding.")
        return
    print("Seeding pathways...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            pathway_entry = Pathway(
                pathway_id=to_str(row.get('pathway_id')),
                from_stop_id=to_str(row.get('from_stop_id')),
                to_stop_id=to_str(row.get('to_stop_id')),
                pathway_mode=to_int(row.get('pathway_mode')),
                is_bidirectional=to_int(row.get('is_bidirectional')),
                length=to_float(row.get('length')),
                traversal_time=to_int(row.get('traversal_time')),
                stair_count=to_int(row.get('stair_count')),
                max_slope=to_float(row.get('max_slope')),
                min_width=to_float(row.get('min_width')),
                signposted_as=to_str(row.get('signposted_as')),
                reversed_signposted_as=to_str(row.get('reversed_signposted_as'))
            )
            db_session.add(pathway_entry)
    db_session.commit()
    print("Pathways seeded.")

def seed_transfers(db_session):
    filepath = os.path.join(DATA_DIR, 'transfers.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping transfers seeding.")
        return
    print("Seeding transfers...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            transfer_entry = Transfer(
                from_stop_id=to_str(row.get('from_stop_id')),
                to_stop_id=to_str(row.get('to_stop_id')),
                transfer_type=to_int(row.get('transfer_type')),
                min_transfer_time=to_int(row.get('min_transfer_time'))
            )
            db_session.add(transfer_entry)
    db_session.commit()
    print("Transfers seeded.")

def seed_fare_attributes(db_session):
    filepath = os.path.join(DATA_DIR, 'fare_attributes.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping fare_attributes seeding.")
        return
    print("Seeding fare_attributes...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fare_attribute_entry = FareAttribute(
                fare_id=to_str(row.get('fare_id')),
                price=to_float(row.get('price')),
                currency_type=to_str(row.get('currency_type')),
                payment_method=to_int(row.get('payment_method')),
                transfers=to_int(row.get('transfers')),
                agency_id=to_str(row.get('agency_id')) if row.get('agency_id') else None,
                transfer_duration=to_int(row.get('transfer_duration'))
            )
            db_session.add(fare_attribute_entry)
    db_session.commit()
    print("Fare_attributes seeded.")

def seed_fare_rules(db_session):
    filepath = os.path.join(DATA_DIR, 'fare_rules.txt')
    if not os.path.exists(filepath):
        print(f"Fichier {filepath} non trouvé. Skipping fare_rules seeding.")
        return
    print("Seeding fare_rules...")
    with open(filepath, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            fare_rule_entry = FareRule(
                fare_id=to_str(row.get('fare_id')),
                route_id=to_str(row.get('route_id')) if row.get('route_id') else None,
                origin_id=to_str(row.get('origin_id')) if row.get('origin_id') else None,
                destination_id=to_str(row.get('destination_id')) if row.get('destination_id') else None,
                contains_id=to_str(row.get('contains_id')) if row.get('contains_id') else None
            )
            db_session.add(fare_rule_entry)
    db_session.commit()
    print("Fare_rules seeded.")
# ***** FIN DES FONCTIONS AJOUTÉES/CORRIGÉES *****


def main():
    db_session = SessionLocal()
    try:
        print("Starting database seeding...")

        # Optionnel: Vider les tables
        # for table in reversed(Base.metadata.sorted_tables):
        #     print(f"Clearing table {table.name}...")
        #     db_session.execute(table.delete())
        # db_session.commit()
        # print("All tables cleared.")

        # Ordre de seeding:
        seed_feed_info(db_session)
        seed_agencies(db_session)
        seed_levels(db_session) # Doit être défini
        seed_stops(db_session)
        seed_calendar(db_session)
        seed_calendar_dates(db_session)
        seed_routes(db_session)
        seed_shapes(db_session) # Mis à jour pour utiliser batching
        
        seed_fare_attributes(db_session) # Doit être défini
        
        seed_trips(db_session)
        
        seed_stop_times(db_session) # Mis à jour pour utiliser batching
        seed_frequencies(db_session) # Doit être défini
        
        seed_pathways(db_session) # Doit être défini
        seed_transfers(db_session) # Doit être défini
        
        seed_fare_rules(db_session) # Doit être défini

        print("Database seeding completed successfully!")
    except Exception as e:
        db_session.rollback()
        print(f"An error occurred during seeding: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db_session.close()

if __name__ == "__main__":
    main()