from pony.orm import db_session, commit, select
from core.models import Booking
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    with db_session:
      bookings = list(select(b for b in Booking if b.book_ref in refs))
  except Exception as e:
    print(f'[ERROR] Test 15 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    with db_session:
      for booking in bookings:
        booking.delete()
        commit()
  except Exception as e:
    print(f'[ERROR] Test 15 failed (delete phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()