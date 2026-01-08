import asyncio
import os
import sys
import time
from sqlalchemy import delete
from tests_async.db import AsyncSessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


async def delete_booking_async():
    refs = [generate_book_ref(i) for i in range(COUNT)]
    async with AsyncSessionLocal() as session:
        async with session.begin():
            stmt = delete(Booking).where(Booking.book_ref.in_(refs))
            await session.execute(stmt)


async def main() -> None:
    start = time.perf_counter_ns()

    try:
        await delete_booking_async()
    except Exception as e:
        print(f'[ERROR] Test 14 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 14. Batch delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
