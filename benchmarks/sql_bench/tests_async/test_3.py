import asyncio
import os
import sys
import time
from datetime import datetime, UTC
from decimal import Decimal

from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal("10.00")


async def main() -> None:
    start = time.perf_counter_ns()

    curr_date = datetime.now(UTC)
    rows = [(generate_book_ref(i), curr_date, generate_amount(i)) for i in range(COUNT)]

    try:
        conn = await get_connection()
        try:
            await conn.executemany(
                """
                INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                VALUES ($1, $2, $3)
                """,
                rows
            )
        finally:
            await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 3 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 3. Bulk create. {COUNT} entities\n'
        f'elapsed_ns={elapsed};'
    )


if __name__ == "__main__":
    asyncio.run(main())
