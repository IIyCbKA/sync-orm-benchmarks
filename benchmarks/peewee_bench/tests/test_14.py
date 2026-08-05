from core.models import Booking
from core.database import db
from core.pg_manager import pg_timer
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 14 failed (data preparation): {e}')
    sys.exit(1)

  try:
    with db.connection_context():
      pg_timer.reset()
      start = time.perf_counter_ns()

      Booking.delete().where(Booking.book_ref.in_(refs)).execute()

      end = time.perf_counter_ns()
      pg_sample = pg_timer.collect()
  except Exception as e:
    print(f'[ERROR] Test 14 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = end - start
  pg_elapsed = pg_sample.total_ns

  print(
    f'Peewee. Test 14. Bulk deletion of {COUNT} objects\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
