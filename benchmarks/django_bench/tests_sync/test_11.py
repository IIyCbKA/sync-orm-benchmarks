from decimal import Decimal
from functools import lru_cache
import os
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
  value = i + 100
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with transaction.atomic():
      for i in range(COUNT):
        booking = Booking.objects.filter(book_ref=generate_book_ref(i)).first()
        if booking:
          booking.total_amount = get_new_amount(i)
          booking.book_date = get_curr_date()
          booking.save(update_fields=['total_amount', 'book_date'])
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 11. Batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed:.0f};'
  )


if __name__ == '__main__':
  main()