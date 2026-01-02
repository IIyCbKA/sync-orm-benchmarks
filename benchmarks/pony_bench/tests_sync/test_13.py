from decimal import Decimal
from pony.orm import db_session, select
from core.models import Booking, Ticket
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      for i in range(COUNT):
        book_ref = generate_book_ref(i)
        select(b for b in Booking if b.book_ref == book_ref).update(
          total_amount=Booking.total_amount + Decimal('10.00')
        )

        select(t for t in Ticket if t.book_ref == book_ref).update(
          passenger_name='Nested update'
        )
  except Exception as e:
    print(f'[ERROR] Test 13 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()