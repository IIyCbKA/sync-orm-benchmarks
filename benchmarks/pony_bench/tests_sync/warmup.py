from datetime import datetime, UTC
from decimal import Decimal
from pony.orm import db_session, commit, flush
from core.models import Booking, Ticket
import os

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))


def warm_up() -> None:
  with db_session:
    for i in range(COUNT):
      try:
        b = Booking(
          book_ref=f'warm{i:02d}',
          book_date=datetime.now(UTC),
          total_amount=Decimal('5.00')
        )
        flush()

        t = Ticket(
          ticket_no=f'warm{i:09d}',
          book_ref=b,
          passenger_id=f'warm{i:05d}',
          passenger_name='Warm',
          outbound=True
        )
        flush()

        _ = Booking.get(book_ref=f'warm{i:02d}')
        __ = Ticket.get(ticket_no=f'warm{i:09d}')

        b.total_amount = Decimal('2.00')
        flush()

        t.passenger_name = 'WarmUpdate'
        flush()

        b.delete()
        flush()
        t.delete()
        commit()
      except Exception:
        pass

  print('Warm-uo done')


if __name__ == '__main__':
  warm_up()
