import asyncio
import sys
import time
from tests_async.db import get_connection

def generate_book_ref(i: int) -> str:
    return f'a{i:05d}'

async def main() -> None:
    start = time.perf_counter_ns()

    try:
        conn = await get_connection()
        await conn.fetchrow("""SELECT 
            tickets.ticket_no, 
            tickets.book_ref, 
            tickets.passenger_id, 
            tickets.passenger_name, 
            tickets.outbound, 
            bookings.book_ref, 
            bookings.book_date, 
            bookings.total_amount
            FROM tickets INNER JOIN bookings ON 
            (tickets.book_ref = bookings.book_ref) 
            WHERE tickets.book_ref = $1""",
                        generate_book_ref(1))

    except Exception as e:
        print(f'[ERROR] Test 9 failed: {e}')
        sys.exit(1)
    finally:
        await conn.close()

    elapsed = time.perf_counter_ns() - start

    print(
        f'Pure async SQL (asyncpg). Test 9. Nested find\n'
        f'elapsed_ns={elapsed};'
    )

if __name__ == "__main__":
    asyncio.run(main())
