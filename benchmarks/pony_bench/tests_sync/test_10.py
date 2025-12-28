from datetime import datetime, timedelta, UTC
from decimal import Decimal
from pony.orm import db_session
from core.models import Booking
import os
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


def main() -> None:
  now = datetime.now(UTC)
  date_from = now - timedelta(days=30)
  amount_low = Decimal('50.00')
  amount_high = Decimal('500.00')
  start = time.perf_counter_ns()

  with db_session():
    try:
      _ = Booking.select(lambda b:
        amount_low <= b.total_amount <= amount_high
        and b.book_date >= date_from
      ).order_by(Booking.total_amount
      ).limit(LIMIT, offset=OFFSET)[:]
    except Exception:
      pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 10. Filter, paginate & sort\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()