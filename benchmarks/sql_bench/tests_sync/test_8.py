import time
import sys
from tests_sync.db import get_connection

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                _ = cur.execute("""
                    SELECT 
                        bookings.book_ref, 
                        bookings.book_date, 
                        bookings.total_amount
                    FROM bookings.bookings 
                    WHERE book_ref = %s LIMIT 1
                """, (generate_book_ref(1),)).fetchone()
    except Exception as e:
        print(f'[ERROR] Test 8 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 8. Find unique\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == '__main__':
    main()
