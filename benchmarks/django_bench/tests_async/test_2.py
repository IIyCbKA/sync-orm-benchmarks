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
from django.db import transaction
from django.utils import timezone

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


@sync_to_async
def batch_create_sync() -> None:
  with transaction.atomic():
    for i in range(COUNT):
      Booking.objects.create(
        book_ref=generate_book_ref(i),
        book_date=get_curr_date(),
        total_amount=generate_amount(i),
      )


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    await batch_create_sync()
  except Exception as e:
    print(f'[ERROR] Test 2 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 2. Transaction create. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())
