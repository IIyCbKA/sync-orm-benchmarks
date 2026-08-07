from sqlalchemy import select, asc
from core.database import SessionLocal
from core.models import Booking
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> tuple[int, int]:
  with SessionLocal() as session:
    pg_timer.reset(session)
    start = time.perf_counter_ns()

    _ = session.scalar(select(Booking).order_by(asc(Booking.book_ref)).limit(1))

    end = time.perf_counter_ns()
    pg_sample = pg_timer.collect()

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
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'SQLModel. Test 5. Retrieval of the first record\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
