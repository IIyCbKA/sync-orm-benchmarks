from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from pony.orm import db_session, commit, select
from core.models import Booking
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
  value = i + 100
  return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  start = time.perf_counter_ns()

  try:
    with db_session:
      for i in range(COUNT):
        select(b for b in Booking if b.book_ref == generate_book_ref(i)).update(
          total_amount=get_new_amount(i),
          book_date=get_curr_date()
        )
        commit()
  except Exception as e:
    print(f'[ERROR] Test 12 failed: {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'PonyORM. Test 12. Single update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()