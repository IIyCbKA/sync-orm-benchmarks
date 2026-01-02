from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from pony.orm import db_session, commit, flush
from core.models import Booking, Ticket
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
  return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
  return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      for i in range(COUNT):
        booking = Booking(
          book_ref=generate_book_ref(i),
          book_date=get_curr_date(),
          total_amount=generate_amount(i)
        )
        flush()

        _ = Ticket(
          ticket_no=generate_ticket_no(i),
          book_ref=booking,
          passenger_id=generate_passenger_id(i),
          passenger_name='Test',
          outbound=True
        )
        commit()
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 4. Nested create. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()