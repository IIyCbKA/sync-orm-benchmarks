from decimal import Decimal
import asyncio
import os
import sys
import time

import django
django.setup()

from asgiref.sync import sync_to_async
from core.models import Booking
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


@sync_to_async
def update_nested_sync(bookings: list[Booking]) -> None:
  with transaction.atomic():
    for booking in bookings:
      booking.total_amount += Decimal('10.00')
      booking.save(update_fields=['total_amount'])
      for ticket in booking.tickets.all():
        ticket.passenger_name = 'Nested update'
        ticket.save(update_fields=['passenger_name'])


async def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    bookings = list(
      Booking.objects
      .filter(book_ref__in=refs)
      .prefetch_related('tickets')
    )
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    await update_nested_sync(bookings)
  except Exception as e:
    print(f'[ERROR] Test 13 failed (update phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 13. Nested transaction update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  asyncio.run(main())