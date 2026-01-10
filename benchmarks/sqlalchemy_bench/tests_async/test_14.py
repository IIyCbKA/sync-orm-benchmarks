import asyncio
import os
import sys
import time
from sqlalchemy import delete, select
from tests_async.db import AsyncSessionLocal
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


async def main() -> None:
    session = AsyncSessionLocal()
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        statement = select(Booking).where(Booking.book_ref.in_(refs))
        result = await session.execute(statement)
        bookings = result.scalars().all()
    except Exception as e:
        print(f'[ERROR] Test 14 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        for booking in bookings:
            await session.delete(booking)
            await session.flush()
        await session.commit()
    except Exception as e:
        print(f'[ERROR] Test 14 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 14. Transaction delete. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
