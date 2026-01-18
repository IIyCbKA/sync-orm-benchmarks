from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import sys
import time
from tests_sync.db import conn

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
    with conn.cursor() as cur:
      cur.execute("""
        UPDATE bookings.bookings
        SET total_amount = total_amount + %s,
            book_date    = %s
        WHERE book_ref = ANY (%s::char(6)[])
      """, (Decimal('10.00'), get_curr_date(), refs))
  except Exception as e:
    print(f'[ERROR] Test 11 failed (update phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Pure SQL (psycopg3). Test 11. Bulk update. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
