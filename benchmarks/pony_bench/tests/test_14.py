from pony.orm import db_session, commit
from core.models import Booking, db
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
    with db_session:
      db.get_connection()
      start = time.perf_counter_ns()

      Booking.select(lambda b: b.book_ref in refs).delete(bulk=True)
      commit()

      end = time.perf_counter_ns()
  except Exception as e:
    print(f'[ERROR] Test 14 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = end - start

  print(
    f'PonyORM. Test 14. Bulk delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
