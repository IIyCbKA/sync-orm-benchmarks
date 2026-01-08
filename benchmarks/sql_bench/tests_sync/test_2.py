from datetime import datetime, UTC
from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.perf_counter_ns()

    rows = []
    curr_date = datetime.now(UTC)
    for i in range(COUNT):
        rows.append((generate_book_ref(i), curr_date, generate_amount(i)))
    connection = get_connection()
    try:
        with connection as conn:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                    VALUES (%s, %s, %s)
                    """,
                    rows,
                )
            conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 2 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 2. Transaction create. {COUNT} entities\n'
        f'elapsed_ns={elapsed};'
    )


if __name__ == "__main__":
    main()
