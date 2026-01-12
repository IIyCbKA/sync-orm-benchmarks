from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
import sys
from tests_sync.db import conn
from psycopg import sql

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.perf_counter_ns()

    try:
        rows = [
            (generate_book_ref(i), get_curr_date(), generate_amount(i))
            for i in range(COUNT)
        ]
        values_sql = sql.SQL(", ").join(
            sql.SQL("(%s, %s, %s)") for _ in rows
        )
        query = sql.SQL("""
            INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
            VALUES {}
        """).format(values_sql)
        with conn.cursor() as cur:
            cur.execute(query, [v for row in rows for v in row])
        conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 3 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 3. Bulk create. {COUNT} entities\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
