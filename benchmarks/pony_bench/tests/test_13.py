from pony.orm import db_session, select, commit
from core.models import Booking
from core.pg_manager import pg_timer
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


@db_session
def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(select(b for b in Booking if b.book_ref in refs))
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  try:
    pg_timer.reset()
    start = time.perf_counter_ns()

    for booking in bookings:
      booking.delete()
    commit()

    end = time.perf_counter_ns()
    pg_sample = pg_timer.collect()
  except Exception as e:
    print(f'[ERROR] Test 13 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = end - start
  pg_elapsed = pg_sample.total_ns

  print(
    f'Pony. Test 13. Deletion of {COUNT} objects in a transaction\n'
    f'elapsed_ns={elapsed}\n'
    f'pg_elapsed_ns={pg_elapsed}'
  )


if __name__ == '__main__':
  main()
