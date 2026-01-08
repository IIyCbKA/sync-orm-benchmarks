import asyncio
import sys
import time
from tests_async.db import get_connection

async def main() -> None:
    start = time.perf_counter_ns()
    first_booking = None

    try:
        conn = await get_connection()
        try:
            first_booking = await conn.fetchrow(
                "SELECT * FROM bookings.bookings ORDER BY book_ref LIMIT 1"
            )
        finally:
            await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 6 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 6. Find first\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
