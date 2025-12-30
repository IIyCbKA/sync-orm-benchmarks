from datetime import datetime
from decimal import Decimal
from dotenv import load_dotenv
from pony.orm import composite_key, Database, PrimaryKey, Required, Set, sql_debug
import os

load_dotenv()

db = Database()

DEBUG = os.environ.get('DEBUG', 'False') == 'True'
sql_debug(DEBUG)

class Booking(db.Entity):
  _table_ = 'bookings'

  book_ref = PrimaryKey(str, max_len=6, sql_type='char(6)')
  book_date = Required(datetime, sql_type='timestamptz')
  total_amount = Required(Decimal, precision=10, scale=2, optimistic=False)

  tickets = Set('Ticket', reverse='book_ref')


class Ticket(db.Entity):
  _table_ = 'tickets'

  ticket_no = PrimaryKey(str, max_len=13, sql_type='text')
  book_ref = Required(Booking)
  passenger_id = Required(str, sql_type='text')
  passenger_name = Required(str, sql_type='text')
  outbound = Required(bool, sql_type='boolean')

  composite_key(book_ref, passenger_id, outbound)


db.bind(
  provider='postgres',
  user=os.environ.get('POSTGRES_USER', 'postgres'),
  password=os.environ.get('POSTGRES_PASSWORD', ''),
  host=os.environ.get('POSTGRES_HOST', 'localhost'),
  database=os.environ.get('POSTGRES_DB', 'postgres'),
)

db.generate_mapping(create_tables=False, check_tables=False)