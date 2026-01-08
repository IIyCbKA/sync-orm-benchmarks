import asyncio
import os
import sys
import time
from sqlalchemy import delete, select
from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'b{i:05d}'



async def delete_booking(i: int):
    async with AsyncSessionLocal() as session:
        try:
            statement = select(Booking).where(Booking.book_ref == generate_book_ref(i)).limit(1)
            result = await session.scalars(statement)
            booking = result.first()
            if booking:
                await session.delete(booking)
                await session.commit()
        except Exception as e:
            print(f'[ERROR] Test 15 failed: {e}')
            sys.exit(1)


sem = asyncio.Semaphore(POOL_SIZE)

async def sem_task(task):
    async with sem:
        return await task

async def main() -> None:
    start = time.perf_counter_ns()

    tasks = [sem_task(delete_booking(i)) for i in range(COUNT)]
    await asyncio.gather(*tasks)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 15. Single delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
