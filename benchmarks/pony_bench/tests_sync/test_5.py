from pony.orm import db_session
from core.models import Booking
import time

def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
        _ = Booking.select()[:]
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 5. Find all\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()