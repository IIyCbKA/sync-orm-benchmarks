from pony.orm import db_session
from core.models import Booking
import sys
import time

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      _ = Booking.get(book_ref=generate_book_ref(1))
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 8. Find unique\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()