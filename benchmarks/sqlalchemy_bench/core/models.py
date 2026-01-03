from decimal import Decimal
from sqlalchemy import Numeric, ForeignKey, CHAR, Text, Boolean, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Booking(Base):
    __tablename__ = "bookings"

    book_ref: Mapped[str] = mapped_column(CHAR(6), primary_key=True)
    book_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric, nullable=False)


    __table_args__ = (
        Index("idx_book_ref", "book_ref"),
    )


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_no: Mapped[str] = mapped_column(Text, primary_key=True)
    book_ref: Mapped[str] = mapped_column(
        ForeignKey("bookings.book_ref"), nullable=False
    )
    passenger_id: Mapped[str] = mapped_column(Text, nullable=False)
    passenger_name: Mapped[str] = mapped_column(Text, nullable=False)
    outbound: Mapped[bool] = mapped_column(Boolean, nullable=False)

    __table_args__ = (
        Index("idx_ticket_no", "ticket_no"),
        UniqueConstraint("book_ref", "passenger_id", "outbound",
                         name="unique_constraint_book_ref_passenger_id_outbound"),
    )
