import asyncio
import sys
from datetime import datetime, timedelta, UTC
from decimal import Decimal
import os
import time
from tests_async.db import get_connection

LIMIT = int(os.environ.get('LIMIT', '250'))
OFFSET = int(os.environ.get('OFFSET', '500'))

async def main() -> None:
    now = datetime.now(UTC)
    date_from = now - timedelta(days=30)
    amount_low = Decimal('50.00')
    amount_high = Decimal('500.00')
    start = time.perf_counter_ns()

    try:
        conn = await get_connection()
        rows = await conn.fetch(
            """
            SELECT *
            FROM bookings.bookings
            WHERE total_amount BETWEEN $1 AND $2
              AND book_date >= $3
            ORDER BY total_amount ASC
            LIMIT $4 OFFSET $5
            """,
            amount_low, amount_high, date_from, LIMIT, OFFSET
        )

    except Exception as e:
        print(f'[ERROR] Test 10 failed: {e}')
        sys.exit(1)
    finally:
        await conn.close()

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 10. Filter, paginate & sort\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
