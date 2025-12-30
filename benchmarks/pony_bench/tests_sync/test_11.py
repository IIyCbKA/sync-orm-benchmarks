from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from pony.orm import db_session, flush
from core.models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
  value = i + 100
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  start = time.perf_counter_ns()

  with db_session:
    try:
      for i in range(COUNT):
        booking = Booking.select(
          lambda b: b.book_ref == generate_book_ref(i)).order_by(
          Booking.book_ref).first()
        if booking:
          booking.total_amount = get_new_amount(i)
          booking.book_date = get_curr_date()
          flush()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 11. Batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()