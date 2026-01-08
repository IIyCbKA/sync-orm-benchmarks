from datetime import datetime, UTC
from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.perf_counter_ns()
    conn = get_connection()
    with conn.cursor() as cur:
        for i in range(COUNT):
            try:
                cur.execute(
                    """
                    INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                    VALUES (%s, %s, %s)
                    """,
                    (
                        generate_book_ref(i),
                        datetime.now(UTC),
                        generate_amount(i),
                    ),
                )
                conn.commit()
            except Exception as e:
                print(f'[ERROR] Test 1 failed: {e}')
                sys.exit(1)
    conn.close()

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 1. Single create. {COUNT} entities\n'
        f'elapsed_ns={elapsed};'
    )


if __name__ == "__main__":
    main()
