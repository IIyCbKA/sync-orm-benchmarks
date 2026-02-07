from decimal import Decimal
from sqlalchemy import select, asc
from core.database import SessionLocal
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
  with SessionLocal() as session:
    start = time.perf_counter_ns()

    stmt = (
      select(Booking)
        .where(Booking.total_amount.between(AMOUNT_LOW, AMOUNT_HIGH))
        .order_by(asc(Booking.total_amount))
        .limit(LIMIT)
        .offset(OFFSET)
    )
    _ = session.scalars(stmt).all()

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
    f'SQLAlchemy (sync). Test 8. Find with filter, offset pagination and sort\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
