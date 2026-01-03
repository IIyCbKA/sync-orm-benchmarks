import asyncio
import os
import time
from sqlalchemy import delete, select
from tests_async.db import AsyncSessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'



async def delete_booking(i: int):
    async with AsyncSessionLocal() as session:
        try:
            stmt_select = select(Booking).where(Booking.book_ref == generate_book_ref(i)).limit(1)
            booking = await session.scalar(stmt_select)
            if booking:
                stmt_delete = delete(Booking).where(Booking.book_ref == booking.book_ref)
                await session.execute(stmt_delete)
                await session.commit()
        except Exception as e:
            print(e)


sem = asyncio.Semaphore(30)

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
