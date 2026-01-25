from sqlalchemy import select
from tests_sync.database import SessionLocal
from core.models import Booking
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def select_iteration() -> int:
  with SessionLocal() as session:
    start = time.perf_counter_ns()

    _ = session.scalars(select(Booking)).all()

    end = time.perf_counter_ns()

  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'SQLModel (sync). Test 4. Find all\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
