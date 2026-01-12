from datetime import datetime, UTC
from decimal import Decimal
from functools import lru_cache
import os
import time
import sys
from tests_sync.db import conn

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def generate_ticket_no(i: int) -> str:
    return f'98{i:11d}'


def generate_passenger_id(i: int) -> str:
    return f'p{i:08d}'


def generate_amount(i: int) -> Decimal:
    value = i + 500
    return Decimal(value) / Decimal('10.00')


@lru_cache(1)
def get_curr_date():
    return datetime.now(UTC)


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with conn.cursor() as cur:
            for i in range(COUNT):
                book_ref = generate_book_ref(i)
                with conn.transaction():
                    cur.execute("""
                        INSERT INTO bookings.bookings (book_ref, book_date, total_amount)
                        VALUES (%s, %s, %s)
                    """, (book_ref, get_curr_date(), generate_amount(i)))

                    cur.execute("""
                        INSERT INTO bookings.tickets 
                        (ticket_no, book_ref, passenger_id, passenger_name, outbound)
                        VALUES (%s, %s, %s, %s, %s)
                    """, (
                        generate_ticket_no(i),
                        book_ref,
                        generate_passenger_id(i),
                        'Test',
                        True,
                    ))
    except Exception as e:
        print(f'[ERROR] Test 4 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 4. Nested create. {COUNT} entities\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()