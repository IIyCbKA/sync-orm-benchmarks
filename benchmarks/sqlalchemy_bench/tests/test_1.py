from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from core.database import SessionLocal
from core.models import Booking
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def create_iteration(i: int) -> tuple[int, int]:
  with SessionLocal() as session:
    pg_timer.reset(session)
    start = time.perf_counter_ns()

    booking = Booking(
      book_ref=generate_book_ref(i),
      book_date=get_curr_date(),
      total_amount=generate_amount(i),
    )
    session.add(booking)
    session.commit()

    end = time.perf_counter_ns()
    pg_sample = pg_timer.collect()

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for i in range(COUNT):
      elapsed_ns, pg_elapsed_ns = create_iteration(i)
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 1 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'SQLAlchemy. Test 1. Single object creation\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
