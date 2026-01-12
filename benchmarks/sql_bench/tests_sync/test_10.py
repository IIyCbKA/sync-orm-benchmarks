from datetime import datetime, timedelta, UTC
from decimal import Decimal
import os
import time
import sys
from tests_sync.db import conn

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))


def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.perf_counter_ns()

    try:
        with conn.cursor() as cur:
            _ = cur.execute("""
                SELECT 
                    bookings.book_ref, 
                    bookings.book_date, 
                    bookings.total_amount
                FROM bookings.bookings
                WHERE total_amount BETWEEN %s AND %s AND book_date >= %s
                ORDER BY total_amount
                LIMIT %s OFFSET %s
            """, (amount_low, amount_high, date_from, LIMIT, OFFSET)).fetchall()
    except Exception as e:
        print(f'[ERROR] Test 10 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 10. Filter, paginate & sort\n'
        f'elapsed_ns={elapsed}'
    )

if __name__ == '__main__':
    main()
