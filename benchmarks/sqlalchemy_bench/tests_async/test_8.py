import asyncio
import time
from sqlalchemy import select
from tests_async.db import AsyncSessionLocal
from core.models import Booking


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


async def main() -> None:
    start = time.perf_counter_ns()

    try:
        async with AsyncSessionLocal() as session:
            stmt = select(Booking).where(Booking.book_ref == generate_book_ref(1)).limit(1)
            booking = await session.scalar(stmt)
    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 8. Find unique\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())