from decimal import Decimal
from pony.orm import db_session, commit
from core.models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  with db_session():
    try:
      for i in range(COUNT):
        booking = Booking.get(book_ref=generate_book_ref(i))
        if booking:
          booking.total_amount += Decimal('10.00')
          for ticket in booking.tickets:
            ticket.passenger_name = 'Nested update'
      commit()
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()