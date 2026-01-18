import os
import statistics
import sys
import time
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'a{i:05d}'


def main() -> None:
  try:
    refs = [generate_book_ref(i) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 12 failed (data preparation): {e}')
    sys.exit(1)

  results: list[int] = []

  try:
    for ref in refs:
      start = time.perf_counter_ns()

      with conn.cursor() as cur:
        cur.execute("""
          DELETE FROM bookings.bookings
          WHERE book_ref IN (%s)
        """, (ref,))

      end = time.perf_counter_ns()
      results.append(end - start)
  except Exception as e:
    print(f'[ERROR] Test 12 failed (delete phase): {e}')
    sys.exit(1)

  elapsed = statistics.median(results)

  print(
    f'Pure SQL (psycopg3). Test 12. Single delete\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
