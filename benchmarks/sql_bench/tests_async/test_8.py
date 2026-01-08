import asyncio
import sys
import time
from tests_async.db import get_connection

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

async def main() -> None:
    start = time.perf_counter_ns()
    booking = None

    try:
        conn = await get_connection()
        try:
            booking = await conn.fetchrow(
                "SELECT * FROM bookings.bookings WHERE book_ref = $1 LIMIT 1",
                generate_book_ref(1)
            )
        finally:
            await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 8 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 8. Find unique\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
