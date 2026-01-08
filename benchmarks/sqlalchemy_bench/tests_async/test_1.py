import asyncio
import sys
from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time

from tests_async.db import AsyncSessionLocal, POOL_SIZE
from core.models import Booking

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'


def generate_amount(i: int) -> Decimal:
    return Decimal(i + 500) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


async def create_booking(i: int) -> None:
    try:
        async with AsyncSessionLocal() as session:
            booking = Booking(
                book_ref=generate_book_ref(i),
                book_date=get_curr_date(),
                total_amount=generate_amount(i),
            )
            session.add(booking)
            await session.commit()
    except Exception as e:
        print(f'[ERROR] Test 1 failed: {e}')
        sys.exit(1)


sem = asyncio.Semaphore(POOL_SIZE)

async def sem_task(task):
    async with sem:
        return await task

async def main() -> None:
    start = time.perf_counter_ns()

    tasks = [sem_task(create_booking(i)) for i in range(COUNT)]
    await asyncio.gather(*tasks)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 1. Single create. {COUNT} entities\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())