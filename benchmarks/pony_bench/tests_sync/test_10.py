from datetime import datetime, timedelta, UTC
from decimal import Decimal
from pony.orm import db_session
from core.models import Booking
import os
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


def main() -> None:
  now = datetime.now(UTC)
  date_from = now - timedelta(days=30)
  amount_low = Decimal('50.00')
  amount_high = Decimal('500.00')
  start = time.perf_counter_ns()

  try:
    with db_session:
      _ = list(Booking.select(lambda b:
        b.total_amount >= amount_low
        and b.total_amount <= amount_high
        and b.book_date >= date_from
      ).order_by(lambda b: b.total_amount)[OFFSET : OFFSET + LIMIT])
  except Exception as e:
    print(f'[ERROR] Test 10 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 10. Filter, paginate & sort\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()