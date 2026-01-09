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
                    tickets = [ticket[0] for ticket in cur.execute("""
                        SELECT ticket_no
                        FROM bookings.tickets
                        WHERE book_ref = %s
                    """, (ref,)).fetchall()]

                    current_data.append((ref, tickets))
    except Exception as e:
        print(f'[ERROR] Test 17 failed (data preparation): {e}')
        sys.exit(1)

    start = time.perf_counter_ns()

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                for ref, tickets in current_data:
                    for ticket_no in tickets:
                        cur.execute("""
                            DELETE FROM bookings.tickets WHERE ticket_no = %s
                        """, (ticket_no,))

                    cur.execute("""
                        DELETE FROM bookings.bookings WHERE book_ref = %s
                    """, (ref,))
                    conn.commit()
    except Exception as e:
        print(f'[ERROR] Test 17 failed (delete phase): {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 17. Nested delete. {COUNT} entries\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
