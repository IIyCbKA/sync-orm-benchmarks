import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    refs = [generate_book_ref(i) for i in range(COUNT)]
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                with conn.transaction():
                    for ref in refs:
                        cur.execute("""
                            DELETE FROM bookings.bookings
                            WHERE book_ref = %s
                        """, (ref,))
    except Exception as e:
        print(f'[ERROR] Test 14 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 14. Transaction delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == '__main__':
    main()
