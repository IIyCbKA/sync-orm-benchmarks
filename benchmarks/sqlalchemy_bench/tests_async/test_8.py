import asyncio
import sys
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
            _ = await session.get(Booking, generate_book_ref(1))
    except Exception as e:
        print(f'[ERROR] Test 8 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f"SQLAlchemy (async). Test 8. Find unique\n"
        f"elapsed_ns={elapsed:.0f};"
    )


if __name__ == "__main__":
    asyncio.run(main())