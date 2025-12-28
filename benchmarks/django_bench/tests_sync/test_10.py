from datetime import timedelta
from decimal import Decimal
import os
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


def main() -> None:
  now = timezone.now()
  date_from = now - timedelta(days=30)
  amount_low = Decimal('50.00')
  amount_high = Decimal('500.00')
  start = time.perf_counter_ns()

  try:
    _ = list(Booking.objects.filter(
      total_amount__gte=amount_low,
      total_amount__lte=amount_high,
      book_date__gte=date_from
    ).order_by('total_amount')[OFFSET:OFFSET + LIMIT])
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 10. Filter, paginate & sort\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()
