from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
import sys
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.perf_counter_ns()

    try:
        params = [
            (generate_book_ref(i), get_curr_date(), generate_amount(i))
            for i in range(COUNT)
        ]

        with conn.cursor() as cur:
            with conn.transaction():
                cur.executemany("""
                    INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                    VALUES (%s, %s, %s)
                """, params)
    except Exception as e:
        print(f'[ERROR] Test 2 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 2. Transaction create. {COUNT} entities\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
