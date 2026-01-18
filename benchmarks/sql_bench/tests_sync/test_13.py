import os
import time
import sys
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
  return f'b{i:05d}'


def main() -> None:
  try:
    refs = [(generate_book_ref(i),) for i in range(COUNT)]
  except Exception as e:
    print(f'[ERROR] Test 13 failed (data preparation): {e}')
    sys.exit(1)

  start = time.perf_counter_ns()

  try:
    with conn.cursor() as cur:
      with conn.transaction():
        cur.executemany("""
          DELETE FROM bookings.bookings
          WHERE book_ref = %s
        """, refs)
  except Exception as e:
    print(f'[ERROR] Test 13 failed (delete phase): {e}')
    sys.exit(1)

  end = time.perf_counter_ns()
  elapsed = end - start

  print(
    f'Pure SQL (psycopg3). Test 13. Transaction delete. {COUNT} entries\n'
    f'elapsed_ns={elapsed}'
  )


if __name__ == '__main__':
  main()
