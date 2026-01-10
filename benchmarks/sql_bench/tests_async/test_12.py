import asyncio
import sys
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
from tests_async.db import get_pool

COUNT = int(os.environ.get("ITERATIONS", "2500"))
POOL_SIZE = 30

def generate_book_ref(i: int) -> str:
    return f"a{i:05d}"

def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal("10.00")

@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)

async def update_booking(pool, i: int) -> None:
    async with pool.acquire() as conn:
        async with conn.transaction():
            await conn.execute(
                """
                UPDATE bookings.bookings
                SET total_amount = $1,
                    book_date = $2
                WHERE book_ref = $3
                """,
                get_new_amount(i),
                get_curr_date(),
                generate_book_ref(i)
            )

async def main() -> None:
    start = time.perf_counter_ns()

    try:
        pool = await get_pool()

        tasks = [update_booking(pool, i) for i in range(COUNT)]
        await asyncio.gather(*tasks)

    except Exception as e:
        print(f"[ERROR] Test 12 failed: {e}")
        sys.exit(1)
    finally:
        await pool.close()

    elapsed = time.perf_counter_ns() - start
    print(
        f"Pure async SQL (asyncpg). Test 12. Single update. {COUNT} entries\n"
        f"elapsed_ns={elapsed};"
    )

if __name__ == "__main__":
    asyncio.run(main())
