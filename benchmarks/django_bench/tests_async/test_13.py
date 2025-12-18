from decimal import Decimal
import asyncio
import os
import time

import django
django.setup()

from core.models import Booking
from django.db import transaction

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


async def main() -> None:
  start = time.perf_counter_ns()

  try:
    async with transaction.atomic():
      for i in range(COUNT):
        booking = await Booking.objects.filter(book_ref=generate_book_ref(i)).afirst()
        if booking:
          booking.total_amount += Decimal('10.00')
          await booking.asave(update_fields=['total_amount'])
          async for ticket in booking.tickets.all():
            ticket.passenger_name = 'Nested update'
            await ticket.asave(update_fields=['passenger_name'])
  except Exception:
    pass

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (async). Test 13. Nested batch update. {COUNT} entries\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  asyncio.run(main())