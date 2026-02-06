from decimal import Decimal
import os
import sys

import django
django.setup()

from core.models import Booking, Ticket
from django.db import transaction
from django.utils import timezone

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))


def warm_up() -> None:
  try:
    for i in range(COUNT):
      with transaction.atomic():
        b = Booking(
          book_ref=f'warm{i:02d}',
          book_date=timezone.now(),
          total_amount=Decimal('5.00')
        )
        b.save()

        t = Ticket(
          ticket_no=f'warm{i:09d}',
          book_ref=b,
          passenger_id=f'warm{i:05d}',
          passenger_name='Warm',
          outbound=True
        )
        t.save()

        _ = Booking.objects.get(book_ref=f'warm{i:02d}')
        __ = Ticket.objects.get(ticket_no=f'warm{i:09d}')

        b.total_amount = Decimal('2.00')
        b.save(update_fields=['total_amount'])

        t.passenger_name = 'WarmUpdate'
        t.save(update_fields=['passenger_name'])

        t.delete()
        b.delete()
  except Exception as e:
    print(f'[ERROR] Warm-up failed: {e}')
    sys.exit(1)

  print('Warm-up done')


if __name__ == '__main__':
  warm_up()
