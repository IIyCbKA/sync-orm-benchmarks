from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from pony.orm import db_session
from core.models import Booking
import os
import sys

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
  value = i + 500
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  """
  Pony ORM does not support true bulk insert.
  Therefore, Test 3 "Bulk create" is skipped for Pony,
  and we mark it with a dash in benchmarks.

  However, to ensure fair comparison in subsequent tests (update, delete, etc.),
  the table must contain the same number of rows as in ORM that support bulk insert.
  This script creates the required number of Booking entities one by one
  to align the dataset size across all tested ORMs.
  """

  try:
    with db_session:
      for i in range(COUNT):
        Booking(
          book_ref=generate_book_ref(i),
          book_date=get_curr_date(),
          total_amount=generate_amount(i),
        )
  except Exception as e:
    print(f'[ERROR] Dataset create failed (instead of bulk create): {e}')
    sys.exit(1)

  print(
    f'PonyORM. Test 3. Bulk create. {COUNT} entities\n'
    f'Bulk create is not supported'
  )


if __name__ == '__main__':
  main()
