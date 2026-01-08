import asyncio
import sys
from decimal import Decimal
from datetime import datetime, UTC
import os
import time
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

async def main() -> None:
    start = time.perf_counter_ns()
    conn = await get_connection()
    try:
        for i in range(COUNT):
            await conn.execute(
                """
                UPDATE bookings.bookings
                SET total_amount = total_amount + $1
                WHERE book_ref = $2
                """,
                Decimal('10.00'),
                generate_book_ref(i)
            )

            await conn.execute(
                """
                UPDATE bookings.tickets t
                SET passenger_name = $1
                FROM bookings.bookings b
                WHERE t.book_ref = b.book_ref AND b.book_ref = $2
                """,
                'Nested update',
                generate_book_ref(i)
            )
        await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 13 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 13. Nested batch update. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
