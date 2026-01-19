from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from sqlalchemy import update
from sqlalchemy.orm import Session
from tests_sync.db import SessionLocal
from core.models import Booking
import os
import sys
import time

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


@lru_cache(1)
def get_curr_date():
  return datetime.now(UTC)


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 11 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    with SessionLocal() as session:
      stmt = (
        update(Booking)
        .where(Booking.book_ref.in_(refs))
        .values(
          total_amount=Booking.total_amount + Decimal('10.00'),
          book_date=get_curr_date(),
        )
      )
      session.execute(stmt)
      session.commit()
  except Exception as e:
    print(f'[ERROR] Test 11 failed (update phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'SQLAlchemy (sync). Test 11. Bulk update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
