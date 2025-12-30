from pony.orm import db_session
from core.models import Booking
import time

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  with db_session:
    try:
      _ = Booking.select(
        lambda b: b.book_ref == generate_book_ref(1)
      ).order_by(Booking.book_ref).first()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 8. Find unique\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()