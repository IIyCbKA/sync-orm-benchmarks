import asyncio
import os
import sys
from decimal import Decimal
from datetime import datetime, UTC
import asyncpg
from tests_async.db import get_connection

COUNT = int(os.environ.get('WARMUP_ITERATIONS', '20'))

def generate_book_ref(i: int) -> str:
    return f"warm{i:02d}"

def generate_ticket_no(i: int) -> str:
    return f"warm{i:09d}"

def generate_passenger_id(i: int) -> str:
    return f"warm{i:05d}"

async def warm_up_single(conn: asyncpg.Connection, i: int) -> None:
    book_ref = generate_book_ref(i)
    ticket_no = generate_ticket_no(i)
    passenger_id = generate_passenger_id(i)
    curr_date = datetime.now(UTC)

    async with conn.transaction():
        # INSERT bookings
        await conn.execute(
            """
            INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
            VALUES ($1, $2, $3)
            """,
            book_ref, curr_date, Decimal("5.00")
        )

        # INSERT tickets
        await conn.execute(
            """
            INSERT INTO bookings.tickets
            (ticket_no, book_ref, passenger_id, passenger_name, outbound)
            VALUES ($1, $2, $3, $4, $5)
            """,
            ticket_no, book_ref, passenger_id, "Warm", True
        )

        # SELECT bookings
        await conn.fetchrow(
            "SELECT book_ref, total_amount FROM bookings.bookings WHERE book_ref = $1",
            book_ref
        )

        # SELECT tickets
        await conn.fetchrow(
            "SELECT ticket_no, passenger_name FROM bookings.tickets WHERE ticket_no = $1",
            ticket_no
        )

        # UPDATE bookings
        await conn.execute(
            "UPDATE bookings.bookings SET total_amount = $1 WHERE book_ref = $2",
            Decimal("2.00"), book_ref
        )

        # UPDATE tickets
        await conn.execute(
            "UPDATE bookings.tickets SET passenger_name = $1 WHERE ticket_no = $2",
            "WarmUpdate", ticket_no
        )

        # DELETE tickets
        await conn.execute(
            "DELETE FROM bookings.tickets WHERE ticket_no = $1",
            ticket_no
        )

        # DELETE bookings
        await conn.execute(
            "DELETE FROM bookings.bookings WHERE book_ref = $1",
            book_ref
        )

async def warm_up() -> None:
    try:
        conn = await get_connection()
        try:
            for i in range(COUNT):
                await warm_up_single(conn, i)
        finally:
            await conn.close()
    except Exception as e:
        print(f"[ERROR] Warm-up failed: {e}")
        sys.exit(1)

    print("Warm-up done")

if __name__ == "__main__":
    asyncio.run(warm_up())
