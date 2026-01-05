from decimal import Decimal
from functools import lru_cache
import asyncio
import os
import sys
import time

import django
django.setup()

from core.models import Booking
from django.utils import timezone

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def get_new_amount(value: Decimal) -> Decimal:
  return value / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


async def update_booking(booking: Booking) -> None:
  booking.total_amount = get_new_amount(booking.total_amount)
  booking.book_date = get_curr_date()
  await booking.asave(update_fields=['total_amount', 'book_date'])


async def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(Booking.objects.filter(book_ref__in=refs))
  except Exception as e:
    print(f'[ERROR] Test 12 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    tasks = [update_booking(booking) for booking in bookings]
    await asyncio.gather(*tasks)
  except Exception as e:
    print(f'[ERROR] Test 12 failed (update phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 12. Single update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())