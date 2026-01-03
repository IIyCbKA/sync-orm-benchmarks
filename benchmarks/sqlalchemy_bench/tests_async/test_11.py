import asyncio
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
from tests_async.db import AsyncSessionLocal
from core.models import Booking
import os
from sqlalchemy import update

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def get_new_amount(i: int) -> Decimal:
    return Decimal(i + 100) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


async def update_booking_async():
    async with AsyncSessionLocal() as session:
        async with session.begin():
            for i in range(COUNT):
                stmt = (
                    update(Booking)
                    .where(Booking.book_ref == generate_book_ref(i))
                    .values(
                        total_amount=get_new_amount(i),
                        book_date=get_curr_date()
                    )
                )
                await session.execute(stmt)


async def main() -> None:
    start = time.perf_counter_ns()

    try:
        await update_booking_async()
    except Exception as e:
        print(e)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 11. Batch update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
