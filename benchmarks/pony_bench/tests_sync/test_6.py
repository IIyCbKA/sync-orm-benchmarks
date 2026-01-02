from pony.orm import db_session
from core.models import Booking
import sys
import time

def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      _ = Booking.select().order_by(Booking.book_ref).first()
  except Exception as e:
    print(f'[ERROR] Test 6 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 6. Find first\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()