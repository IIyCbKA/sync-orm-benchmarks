from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from pony.orm import db_session, commit
from core.models import Booking
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


@db_session
def update_iteration(i: int) -> tuple[int, int]:
  booking = Booking.get(book_ref=generate_book_ref(i))

  pg_timer.reset()
  start = time.perf_counter_ns()

  booking.total_amount /= Decimal('10.00')
  booking.book_date = get_curr_date()
  commit()

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for i in range(COUNT):
      elapsed_ns, pg_elapsed_ns = update_iteration(i)
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 9 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Pony. Test 9. Single object update\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
