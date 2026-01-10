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



from sqlalchemy import delete

async def delete_booking(book_ref: str):
    async with sem:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    delete(Booking).where(Booking.book_ref == book_ref)
                )



sem = asyncio.Semaphore(POOL_SIZE)

async def main():
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(
                select(Booking.book_ref).where(
                    Booking.book_ref.in_(
                        generate_book_ref(i) for i in range(COUNT)
                    )
                )
            )
            refs = result.scalars().all()
    except Exception as e:
        print(f'[ERROR] Test 15 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    await asyncio.gather(
        *(delete_booking(ref) for ref in refs)
    )

    elapsed = time.perf_counter_ns() - start

    print(
        f"SQLAlchemy (async). Test 15. Single delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )

if __name__ == "__main__":
    asyncio.run(main())
