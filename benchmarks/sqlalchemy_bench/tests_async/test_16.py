import asyncio
import os
import sys
import time
from sqlalchemy import delete, select
from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'c{i:05d}'



sem = asyncio.Semaphore(POOL_SIZE)

async def sem_task(task):
    async with sem:
        return await task

async def main() -> None:
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
    except Exception as e:
        print(f'[ERROR] Test 16 failed (data preparation): {e}')
        sys.exit(1)
    session = AsyncSessionLocal()

    start = time.perf_counter_ns()

    try:
        async with session:
            async with session.begin():
                await session.execute(
                    delete(Booking).where(Booking.book_ref.in_(refs))
                )
    except Exception as e:
        print(f"[ERROR] Test 16 failed (delete phase): {e}")
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 16. Bulk delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
