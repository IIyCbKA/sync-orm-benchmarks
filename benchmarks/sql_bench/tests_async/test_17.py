import os
import time
import sys
import asyncio
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'

async def main() -> None:
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
    except Exception as e:
        print(f"[ERROR] Test 17 failed (data preparation): {e}")
        sys.exit(1)

    start = time.perf_counter_ns()
    conn = await get_connection()
    try:
        for book_ref in refs:
            async with conn.transaction():
                await conn.execute(
                    "DELETE FROM bookings.tickets WHERE book_ref = $1",
                    book_ref
                )
                await conn.execute(
                    "DELETE FROM bookings.bookings WHERE book_ref = $1",
                    book_ref
                )
    except Exception as e:
        print(f"[ERROR] Test 17 failed (delete phase): {e}")
        sys.exit(1)
    await conn.close()
    elapsed = time.perf_counter_ns() - start
    print(
        f'Pure async SQL (asyncpg). Test 17. Nested delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
