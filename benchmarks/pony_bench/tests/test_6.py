from pony.orm import db_session
from core.models import Booking, db
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@db_session
def select_iteration() -> tuple[int, int]:
  db.get_connection()

  pg_timer.reset()
  start = time.perf_counter_ns()

  booking = Booking.get(book_ref=generate_book_ref(1))

  end = time.perf_counter_ns()
  pg_sample = pg_timer.collect()

  if booking is None:
    raise AssertionError('Expected booking, got None')

  return end - start, pg_sample.total_ns


def main() -> None:
  elapsed_results: list[int] = []
  pg_results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      elapsed_ns, pg_elapsed_ns = select_iteration()
      elapsed_results.append(elapsed_ns)
      pg_results.append(pg_elapsed_ns)
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'Pony. Test 6. Retrieval by primary key\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
