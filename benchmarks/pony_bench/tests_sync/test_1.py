from datetime import datetime, UTC
from decimal import Decimal
from pony.orm import db_session, commit
from core.models import Booking
import os
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


def main() -> None:
  start = time.time()

  for i in range(COUNT):
    with db_session():
      try:
        Booking(
          book_ref=generate_book_ref(i),
          book_date=datetime.now(UTC),
          total_amount=generate_amount(i),
        )

        commit()
      except Exception:
        pass

  end = time.time()
  elapsed = end - start

  print(
    f'PonyORM. Test 1. Insert\n'
    f'elapsed_sec={elapsed:.4f};'
  )


if __name__ == '__main__':
  main()
