import time
import sys
from tests_sync.db import conn

def main() -> None:
    start = time.perf_counter_ns()

    try:
        with conn.cursor() as cur:
            _ = cur.execute("""
                SELECT 
                    bookings.book_ref, 
                    bookings.book_date, 
                    bookings.total_amount 
                FROM bookings
            """).fetchall()
    except Exception as e:
        print(f'[ERROR] Test 5 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 5. Find all\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == '__main__':
    main()
