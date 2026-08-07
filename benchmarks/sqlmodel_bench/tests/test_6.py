from sqlalchemy import select
from core.database import SessionLocal
from core.models import Booking
from core.pg_manager import pg_timer
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def select_iteration() -> tuple[int, int]:
  with SessionLocal() as session:
    pg_timer.reset(session)
    start = time.perf_counter_ns()

    _ = session.scalar(
      select(Booking).where(Booking.book_ref == generate_book_ref(1))
    )

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
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(elapsed_results)
  pg_elapsed = statistics.median(pg_results)

  print(
    f'SQLModel. Test 6. Retrieval by primary key\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
