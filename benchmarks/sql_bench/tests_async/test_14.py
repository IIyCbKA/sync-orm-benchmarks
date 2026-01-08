import asyncio
import os
import sys
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
                DELETE FROM bookings.tickets
                USING bookings.bookings b
                WHERE tickets.book_ref = b.book_ref AND b.book_ref = $1
                """,
                generate_book_ref(i)
            )
            await conn.execute(
                """
                DELETE FROM bookings.bookings
                WHERE book_ref = $1
                """,
                generate_book_ref(i)
            )
        await conn.close()
    except Exception as e:
        print(f'[ERROR] Test 14 failed: {e}')
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start
    print(
        f'Pure async SQL (asyncpg). Test 14. Batch delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
