from tests_sync.db import conn
from datetime import datetime, timedelta, UTC
from decimal import Decimal
import os
import statistics
import sys
import time

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))
SELECT_REPEATS = int(os.environ.get('SELECT_REPEATS', '75'))

NOW = datetime.now(UTC)
DATE_FROM = NOW - timedelta(days=30)
AMOUNT_LOW = Decimal('50.00')
AMOUNT_HIGH = Decimal('500.00')


def select_iterations() -> int:
  start = time.perf_counter_ns()

  with conn.cursor() as cur:
    _ = cur.execute("""
      SELECT 
        bookings.book_ref,
        bookings.book_date,
        bookings.total_amount
      FROM bookings.bookings
      WHERE total_amount BETWEEN %s AND %s AND book_date >= %s
      ORDER BY total_amount
      LIMIT %s
      OFFSET %s
    """, (AMOUNT_LOW, AMOUNT_HIGH, DATE_FROM, LIMIT, OFFSET)).fetchall()

  end = time.perf_counter_ns()
  return end - start


def main() -> None:
  results: list[int] = []

  try:
    for _ in range(SELECT_REPEATS):
      results.append(select_iterations())
  except Exception as e:
    print(f'[ERROR] Test 8 failed: {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Pure SQL (psycopg3). Test 8. Find with filter, offset pagination and sort\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
