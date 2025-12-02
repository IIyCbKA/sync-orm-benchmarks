from datetime import datetime, time, timedelta
from decimal import Decimal
from dotenv import load_dotenv
from pony.orm import (
  IntArray,
  composite_index,
  composite_key,
  Database,
  Json,
  Optional,
  PrimaryKey,
  Required,
  Set,
)
import os

load_dotenv()

db = Database()

class Booking(db.Entity):
  _table_ = 'bookings'

  book_ref = PrimaryKey(str, max_length=6, sql_type='char(6)')
  book_date = Required(datetime, sql_type='timestamptz')
  total_amount = Required(Decimal, precision=10, scale=2)

  tickets = Set('Ticket', reverse='book_ref')


class Ticket(db.Entity):
  _table_ = 'tickets'

  ticket_no = PrimaryKey(str, sql_type='text')
  book_ref = Required(Booking)
  passenger_id = Required(str, sql_type='text')
  passenger_name = Required(str, sql_type='text')
  outbound = Required(bool, sql_type='boolean')

  composite_key(book_ref, passenger_id, outbound)

  segments = Set('Segment', reverse='ticket_no')


class Flight(db.Entity):
  _table_ = 'flights'

  flight_id = PrimaryKey(int)
  route_no = Required(str, sql_type='text')
  status = Required(str, sql_type='text')
  scheduled_departure = Required(datetime, sql_type='timestamptz')
  scheduled_arrival = Required(datetime, sql_type='timestamptz')
  actual_departure = Optional(datetime, sql_type='timestamptz')
  actual_arrival = Optional(datetime, sql_type='timestamptz')

  composite_key(route_no, scheduled_departure)

  segments = Set('Segment', reverse='flight_id')


class Segment(db.Entity):
  _table_ = 'segments'

  ticket_no = Required(Ticket)
  flight_id = Required(Flight, index=True)
  fare_conditions = Required(str, sql_type='text')
  price = Required(Decimal, precision=10, scale=2)

  PrimaryKey(ticket_no, flight_id)


class AirplaneData(db.Entity):
  _table_ = 'airplanes_data'

  airplane_code = PrimaryKey(str, max_length=3, sql_type='char(3)')
  model = Required(Json)
  range = Required(int)
  speed = Required(int)

  routes = Set('Route', reverse='airplane_code')
  seats = Set('Seat', reverse='airplane_code', cascade_delete=True)


class AirportData(db.Entity):
  _table_ = 'airports_data'

  airport_code = PrimaryKey(str, max_length=3, sql_type='char(3)')
  airport_name = Required(Json)
  city = Required(Json)
  country = Required(Json)
  coordinates = Required(str, sql_type='point')
  timezone = Required(str, sql_type='text')

  departure_routes = Set('Route', reverse='departure_airport')
  arrival_routes = Set('Route', reverse='arrival_airport')


class Seat(db.Entity):
  _table_ = 'seats'

  airplane_code = Required(AirplaneData)
  seat_no = Required(str, sql_type='text')
  fare_conditions = Required(str, sql_type='text')

  PrimaryKey(airplane_code, seat_no)


class BoardingPass(db.Entity):
  _table_ = 'boarding_passes'

  ticket_no = Required(Ticket)
  flight_id = Required(Flight)
  seat_no = Required(str, sql_type='text')
  boarding_no = Optional(int)
  boarding_time = Optional(datetime, sql_type='timestamptz')

  PrimaryKey(ticket_no, flight_id)
  composite_key(flight_id, boarding_no)
  composite_key(flight_id, seat_no)


class Route(db.Entity):
  _table_ = 'routes'

  route_no = Required(str, sql_type='text')
  validity = Required(str, sql_type='tstzrange')
  departure_airport = Required(AirportData)
  arrival_airport = Required(AirportData)
  airplane_code = Required(AirplaneData)
  days_of_week = Required(IntArray)
  scheduled_time = Required(time, sql_type='time')
  duration = Required(timedelta, sql_type='interval')

  PrimaryKey(route_no, validity)
  composite_index(departure_airport, validity)


db.bind(
  provider='postgres',
  user=os.environ.get('POSTGRES_USER', 'postgres'),
  password=os.environ.get('POSTGRES_PASSWORD', ''),
  host=os.environ.get('POSTGRES_HOST', 'localhost'),
  db=os.environ.get('POSTGRES_DB', 'postgres'),
)

db.generate_mapping(create_tables=False)