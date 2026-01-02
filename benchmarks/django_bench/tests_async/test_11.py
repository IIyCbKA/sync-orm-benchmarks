from decimal import Decimal
from functools import lru_cache
import asyncio
import os
import sys
import time

import django
django.setup()

from asgiref.sync import sync_to_async
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


@sync_to_async
def update_booking_sync() -> None:
  with transaction.atomic():
    for i in range(COUNT):
      Booking.objects.filter(book_ref=generate_book_ref(i)).update(
        total_amount=get_new_amount(i),
        book_date=get_curr_date()
      )


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    await update_booking_sync()
  except Exception as e:
    print(f'[ERROR] Test 11 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 11. Batch update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())