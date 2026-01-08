from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal("10.00")

@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)

def main() -> None:
    start = time.perf_counter_ns()

    conn = get_connection()
    try:
        with conn.cursor() as cur:
            for i in range(COUNT):

                cur.execute(
                    """
                    UPDATE bookings.bookings
                    SET total_amount = %s,
                        book_date = %s
                    WHERE book_ref = %s
                    """,
                    (get_new_amount(i), get_curr_date(), generate_book_ref(i))
                )
            conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 12 failed: {e}')
        sys.exit(1)
    conn.close()

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 12. Single update. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    main()
