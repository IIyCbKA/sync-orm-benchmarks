from pony.orm import db_session, commit
from core.models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    for i in range(COUNT):
      try:
        booking = Booking.get(book_ref=generate_book_ref(i))
        if booking:
          booking.delete()
          commit()
      except Exception:
        pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 15. Single delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()