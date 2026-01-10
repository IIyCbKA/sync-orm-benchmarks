import asyncio
import os
import sys
import time
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache

from sqlalchemy import select, update
from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking

COUNT = int(os.environ.get("ITERATIONS", "2500"))


def generate_book_ref(i: int) -> str:
    return f"a{i:05d}"


def get_new_amount(value: Decimal) -> Decimal:
    return value / Decimal("10.00")


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


sem = asyncio.Semaphore(POOL_SIZE)


async def update_booking(book_ref: str, amount: Decimal):
    async with sem:
        async with AsyncSessionLocal() as session:
            async with session.begin():
                await session.execute(
                    update(Booking)
                    .where(Booking.book_ref == book_ref)
                    .values(
                        total_amount=get_new_amount(amount),
                        book_date=get_curr_date(),
                    )
                )


async def main() -> None:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(Booking.book_ref, Booking.total_amount)
            .where(Booking.book_ref.in_(
                generate_book_ref(i) for i in range(COUNT)
            ))
        )
        rows = result.all()

    start = time.perf_counter_ns()

    tasks = [
        update_booking(book_ref, amount)
        for book_ref, amount in rows
    ]
    await asyncio.gather(*tasks)

    elapsed = time.perf_counter_ns() - start

    print(
        f"SQLAlchemy (async). Test 12. Single update. {COUNT} entries\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())
