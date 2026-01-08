import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'

def main() -> None:
    start = time.perf_counter_ns()
    refs = [generate_book_ref(i) for i in range(COUNT)]
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM bookings.bookings
                WHERE book_ref = ANY(%s)
                """,
                (refs,)
            )
            conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 16 failed: {e}')
        sys.exit(1)
    conn.close()
    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 16. Bulk delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    main()
