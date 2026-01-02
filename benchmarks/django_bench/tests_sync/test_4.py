from decimal import Decimal
from functools import lru_cache
import os
import sys
import time

import django
django.setup()

from core.models import Booking, Ticket
from django.db import transaction
from django.utils import timezone

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
  return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
  return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return timezone.now()


def main() -> None:
  start = time.perf_counter_ns()

  try:
    for i in range(COUNT):
      with transaction.atomic():
        booking = Booking.objects.create(
          book_ref=generate_book_ref(i),
          book_date=get_curr_date(),
          total_amount=generate_amount(i),
        )

        _ = Ticket.objects.create(
          ticket_no=generate_ticket_no(i),
          book_ref=booking,
          passenger_id=generate_passenger_id(i),
          passenger_name='Test',
          outbound=True
        )
  except Exception as e:
    print(f'[ERROR] Test 4 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Django ORM (sync). Test 4. Nested create. {COUNT} entities\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
