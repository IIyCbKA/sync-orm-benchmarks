import asyncio
import os
import time
import sys
from tests_async.db import get_pool

COUNT = int(os.environ.get("ITERATIONS", "2500"))
POOL_SIZE = 30

def generate_book_ref(i: int) -> str:
    return f"b{i:05d}"

async def delete_booking(pool, i: int) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                DELETE FROM bookings.bookings
                WHERE book_ref = $1
                """,
                generate_book_ref(i)
            )

async def main() -> None:
    start = time.perf_counter_ns()

    try:
        pool = await get_pool()

        tasks = [delete_booking(pool, i) for i in range(COUNT)]
        await asyncio.gather(*tasks)

        await pool.close()

    except Exception as e:
        print(f"[ERROR] Test 15 failed: {e}")
        sys.exit(1)

    elapsed = time.perf_counter_ns() - start
    print(
        f"Pure async SQL (asyncpg). Test 15. Single delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed};"
    )

if __name__ == "__main__":
    asyncio.run(main())
