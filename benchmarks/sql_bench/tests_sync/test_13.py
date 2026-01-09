from decimal import Decimal
import os
import time
import sys
from tests_sync.db import get_connection

COUNT = int(os.environ.get('ITERATIONS', '2500'))


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def main() -> None:
    try:
        refs = [generate_book_ref(i) for i in range(COUNT)]
        current_data = []
        with get_connection() as conn:
            with conn.cursor() as cur:
                for ref in refs:
                    total_amount = cur.execute("""
                        SELECT total_amount
                        FROM bookings.bookings
                        WHERE book_ref = %s
                    """, (ref,)).fetchone()[0]

                    tickets = [ticket[0] for ticket in cur.execute("""
                        SELECT ticket_no
                        FROM bookings.tickets
                        WHERE book_ref = %s
                    """, (ref,)).fetchall()]

                    current_data.append((ref, total_amount, tickets))
    except Exception as e:
        print(f'[ERROR] Test 13 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for ref, old_amount, tickets in current_data:
                    with conn.transaction():
                        cur.execute("""
                            UPDATE bookings.bookings
                            SET total_amount = %s
                            WHERE book_ref = %s
                        """, total_amount + Decimal('10.00'), ref)

                        for ticket_no in tickets:
                            cur.execute("""
                                UPDATE bookings.tickets
                                SET passenger_name = %s
                                WHERE ticket_no = %s
                            """, ('Nested update', ticket_no))
    except Exception as e:
        print(f'[ERROR] Test 13 failed (update phase): {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 13. Nested update. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
