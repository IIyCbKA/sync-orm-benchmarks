from datetime import datetime, timedelta, UTC
from decimal import Decimal
from pony.orm import db_session
from core.models import Booking
import time

def main() -> None:
  now = datetime.now(UTC)
  date_from = now - timedelta(days=30)
  amount_low = Decimal('50.00')
  amount_high = Decimal('500.00')
  start = time.time()

  with db_session():
    try:
      Booking.select(lambda b:
        amount_low <= b.total_amount <= amount_high and b.book_date >= date_from
      ).count()
    except Exception:
      pass

  end = time.time()
  elapsed = end - start

  print(
    f'PonyORM. Test 4. Filter large\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()