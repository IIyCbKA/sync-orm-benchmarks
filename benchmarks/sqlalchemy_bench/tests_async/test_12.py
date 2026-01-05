import asyncio
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from sqlalchemy import select, update
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


async def update_booking(i: int):
    async with AsyncSessionLocal() as session:
        try:
            statement = select(Booking).where(Booking.book_ref == generate_book_ref(i)).order_by(Booking.book_ref).limit(1)
            result = await session.scalars(statement)
            booking = result.first()
            if booking:
                booking.total_amount = get_new_amount(i)
                booking.book_date = get_curr_date()
                await session.commit()
        except Exception as e:
            print(e)

sem = asyncio.Semaphore(30)

async def sem_task(task):
    async with sem:
        return await task


async def main() -> None:
    start = time.perf_counter_ns()

    tasks = [sem_task(update_booking(i)) for i in range(COUNT)]
    await asyncio.gather(*tasks)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 12. Single update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
