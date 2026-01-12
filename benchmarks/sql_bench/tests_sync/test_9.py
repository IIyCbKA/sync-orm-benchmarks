import time
import sys
from tests_sync.db import conn


def generate_book_ref(i: int) -> str:
    return f'd{i:05d}'


def main() -> None:
    start = time.perf_counter_ns()

    try:
        with conn.cursor() as cur:
            _ = cur.execute("""
                SELECT 
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
                WHERE tickets.book_ref = %s
            """, (generate_book_ref(1),)).fetchall()
    except Exception as e:
        print(f'[ERROR] Test 9 failed: {e}')
        sys.exit(1)

    end = time.perf_counter_ns()
    elapsed = end - start

    print(
        f'Pure SQL (psycopg3). Test 9. Nested find\n'
        f'elapsed_ns={elapsed}'
    )


if __name__ == '__main__':
    main()
