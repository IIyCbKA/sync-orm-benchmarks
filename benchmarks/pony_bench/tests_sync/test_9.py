from pony.orm import db_session
from core.models import Booking
import time

def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      book = Booking.get(book_ref=generate_book_ref(1))
      if book:
        _ = list(book.tickets)
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 9. Nested find unique\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()