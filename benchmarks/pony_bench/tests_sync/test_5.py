from pony.orm import db_session
from core.models import Booking
import sys
import time

def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      _ = list(Booking.select())
  except Exception as e:
    print(f'[ERROR] Test 5 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 5. Find all\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()