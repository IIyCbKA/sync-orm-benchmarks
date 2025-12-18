from pony.orm import db_session
from core.models import Booking
import time

def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      book = Booking.select().first()
      if book:
        _ = list(book.tickets)
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 7. Nested find first\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()