from pony.orm import db_session
from core.models import Booking, db
import os
import statistics
import sys
import time

SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@db_session
def select_iteration() -> int:
  db.get_connection()
  start = time.perf_counter_ns()

  _ = Booking.get(book_ref=generate_book_ref(1))

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'PonyORM. Test 6. Find unique record\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()