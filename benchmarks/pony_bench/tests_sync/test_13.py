from decimal import Decimal
from pony.orm import db_session, select, flush
from core.models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]

    with db_session:
      bookings = list(select(
        b for b in Booking if b.book_ref in refs).prefetch(Booking.tickets))

      for booking in bookings:
        booking.total_amount += Decimal('10.00')
        flush()
        for ticket in booking.tickets:
          ticket.passenger_name = 'Nested update'
          flush()
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()