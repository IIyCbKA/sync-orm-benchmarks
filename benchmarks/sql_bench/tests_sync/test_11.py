from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
import sys
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
        current_values = []
        with conn.cursor() as cur:
            for ref in refs:
                total_amount = cur.execute("""
                    SELECT total_amount 
                    FROM bookings.bookings
                    WHERE book_ref = %s
                """, (ref,)).fetchone()[0]
                current_values.append((ref, total_amount))
    except Exception as e:
        print(f'[ERROR] Test 11 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        params = [
            (old_amount / Decimal('10.00'), get_curr_date(), book_ref)
            for book_ref, old_amount in current_values
        ]

        with conn.cursor() as cur:
            with conn.transaction():
                cur.executemany("""
                    UPDATE bookings.bookings
                    SET total_amount = %s,
                        book_date    = %s
                    WHERE book_ref = %s
                """, params)
    except Exception as e:
        print(f'[ERROR] Test 11 failed (update phase): {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 11. Transaction update. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
