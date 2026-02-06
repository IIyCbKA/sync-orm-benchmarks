from datetime import datetime, UTC
from decimal import Decimal
from core.database import db
from core.models import Booking, Ticket
import os
import sys

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))


def warm_up() -> None:
  try:
    with db.connection_context():
      for i in range(COUNT):
        with db.atomic():
          b = Booking.create(
            book_ref=f'warm{i:02d}',
            book_date=datetime.now(UTC),
            total_amount=Decimal('5.00')
          )

          t = Ticket.create(
            ticket_no=f'warm{i:09d}',
            book_ref=b,
            passenger_id=f'warm{i:05d}',
            passenger_name='Warm',
            outbound=True
          )

          _ = Booking.get_by_id(f'warm{i:02d}')
          __ = Ticket.get_by_id(f'warm{i:09d}')

          b.total_amount = Decimal('2.00')
          b.save(only=[Booking.total_amount])

          t.passenger_name = 'WarmUpdate'
          t.save(only=[Ticket.passenger_name])

          t.delete_instance()
          b.delete_instance()
  except Exception as e:
    print(f'[ERROR] Warm-up failed: {e}')
    sys.exit(1)

  print('Warm-up done')


if __name__ == '__main__':
  warm_up()