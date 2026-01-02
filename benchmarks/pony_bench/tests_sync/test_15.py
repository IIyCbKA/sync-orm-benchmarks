from pony.orm import db_session, commit, select
from core.models import Booking
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      for i in range(COUNT):
        select(b for b in Booking if b.book_ref == generate_book_ref(i)).delete(bulk=True)
        commit()
  except Exception as e:
    print(f'[ERROR] Test 15 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()