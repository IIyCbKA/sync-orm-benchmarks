import os
import time
import sys
import asyncio
from tests_async.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))

def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'

async def main() -> None:
    start = time.perf_counter_ns()
    refs = [generate_book_ref(i) for i in range(COUNT)]
    conn = await get_connection()
    try:
        async with conn.transaction():
            await conn.execute(
                """
                DELETE FROM bookings.bookings
                WHERE book_ref = ANY($1)
                """,
                refs
            )
    except Exception as e:
        print(f'[ERROR] Test 16 failed: {e}')
        sys.exit(1)
    await conn.close()
    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 16. Bulk delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
