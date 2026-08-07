from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from sqlalchemy import select
from core.database import SessionLocal
from core.models import Booking
from core.pg_manager import pg_timer
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  with SessionLocal() as session:
    try:
      refs = [generate_book_ref(i) for i in range(COUNT)]
      stmt = select(Booking).where(Booking.book_ref.in_(refs))
      bookings = session.execute(stmt).scalars().all()
      session.commit()
    except Exception as e:
      print(f'[ERROR] Test 10 failed (data preparation): {e}')
      sys.exit(1)

    try:
      pg_timer.reset(session)
      start = time.perf_counter_ns()

      for booking in bookings:
        booking.total_amount /= Decimal('10.00')
        booking.book_date = get_curr_date()

      session.commit()

      end = time.perf_counter_ns()
      pg_sample = pg_timer.collect()
    except Exception as e:
      print(f'[ERROR] Test 10 failed (update phase): {e}')
      sys.exit(1)

  elapsed = end - start
  pg_elapsed = pg_sample.total_ns

  print(
    f'SQLModel. Test 10. Update of {COUNT} objects in a transaction\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
