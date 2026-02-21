from decimal import Decimal
from core.database import db
from core.models import Booking
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))

AMOUNT_LOW = Decimal('50.00')
AMOUNT_HIGH = Decimal('500.00')


def select_iteration() -> int:
  with db.connection_context():
    start = time.perf_counter_ns()

    _ = list(Booking
      .select()
      .where(
        (Booking.total_amount >= AMOUNT_LOW)
        & (Booking.total_amount <= AMOUNT_HIGH)
      )
      .order_by(Booking.total_amount)
      .offset(OFFSET)
      .limit(LIMIT))

    end = time.perf_counter_ns()

  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iteration())
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Peewee. Test 8. Filtered retrieval with offset pagination and sorting\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()