from datetime import datetime, UTC
from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection
from psycopg import sql
COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


def main() -> None:
    start = time.perf_counter_ns()

    curr_date = datetime.now(UTC)

    rows = [
        (generate_book_ref(i), curr_date, generate_amount(i))
        for i in range(COUNT)
    ]
    values_sql = sql.SQL(", ").join(
        sql.SQL("(%s, %s, %s)") for _ in rows
    )
    query = sql.SQL("""
        INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
        VALUES {}
    """).format(values_sql)
    connection = get_connection()
    try:
        with connection as conn:
            with conn.cursor() as cur:
                cur.execute(query, [v for row in rows for v in row])
            conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 3 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure SQL (psycopg3). Test 3. Bulk create. {COUNT} entities\n'
        f'elapsed_ns={elapsed};'
    )


if __name__ == "__main__":
    main()
