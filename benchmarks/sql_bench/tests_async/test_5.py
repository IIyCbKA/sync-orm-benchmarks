import asyncio
import sys
import time
from tests_async.db import get_connection

async def main() -> None:
    start = time.perf_counter_ns()
    all_bookings = []

    try:
        conn = await get_connection()
        try:
            all_bookings = await conn.fetch("SELECT * FROM bookings.bookings")
        finally:
            await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 5 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 5. Find all\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
