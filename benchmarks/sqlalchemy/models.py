from geoalchemy2 import Geometry
from sqlalchemy import Integer, Numeric, ForeignKey, CHAR, Text, Boolean, Time, Interval, ForeignKeyConstraint, Index, \
    UniqueConstraint, text
from sqlalchemy.dialects.postgresql import JSONB, TSTZRANGE, ARRAY, TIMESTAMP, ExcludeConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AirplaneData(Base):
    __tablename__ = "airplanes_data"

    airplane_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    model: Mapped[dict] = mapped_column(JSONB, nullable=False)
    range: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (
        Index("idx_airplane_code", "airplane_code"),
    )


class AirportData(Base):
    __tablename__ = "airports_data"

    airport_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    airport_name: Mapped[str] = mapped_column(JSONB, nullable=False)
    city: Mapped[str] = mapped_column(JSONB, nullable=False)
    country: Mapped[str] = mapped_column(JSONB, nullable=False)
    coordinates: Mapped[str] = mapped_column(Geometry(geometry_type='POINT'), nullable=False)
    timezone: Mapped[str] = mapped_column(Text, nullable=False)

    __table_args__ = (
        Index("idx_airport_code", "airport_code"),
    )


class Booking(Base):
    __tablename__ = "bookings"

    book_ref: Mapped[str] = mapped_column(CHAR(6), primary_key=True)
    book_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric, nullable=False)

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


class Flight(Base):
    __tablename__ = "flights"

    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    route_no: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_departure: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    scheduled_arrival: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    actual_departure: Mapped[str | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    actual_arrival: Mapped[str | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )

    __table_args__ = (
        Index("idx_flight_id", "flight_id"),
        UniqueConstraint("route_no", "scheduled_departure", name="unique_constrain_flight_id_scheduled_departure"),
    )


class BoardingPass(Base):
    __tablename__ = "boarding_passes"

    ticket_no: Mapped[str] = mapped_column(Text, primary_key=True)
    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    seat_no: Mapped[str] = mapped_column(Text)
    boarding_no: Mapped[int] = mapped_column(Integer)
    boarding_time: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    __table_args__ = (
        ForeignKeyConstraint(["ticket_no", "flight_id"],
                             ["segments.ticket_no", "segments.flight_id"]),
        Index("idx_ticket_no", "flight_id", "ticket_no"),
        UniqueConstraint("flight_id", "boarding_no", name="unique_constrain_flight_id_boarding_no"),
        UniqueConstraint("flight_id", "seat_no", name="unique_constrain_flight_id_seat_no")
    )


class Seat(Base):
    __tablename__ = "seats"

    airplane_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True)
    seat_no: Mapped[str] = mapped_column(Text, primary_key=True)
    fare_conditions: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        ForeignKeyConstraint(
            ["airplane_code"],
            ["airplanes_data.airplane_code"],
            ondelete="CASCADE"
        ),
        Index("idx_airplane_code_seat_no", "airplane_code", "seat_no"),
    )


class Segment(Base):
    __tablename__ = "segments"
    ticket_no: Mapped[str] = mapped_column(Text, primary_key=True)
    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    fare_conditions: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(["ticket_no"],
                             ["tickets.ticket_no"]),
        ForeignKeyConstraint(["flight_id"],
                             ["flights.flight_id"]),
        Index("idx_ticket_no_flight_id", "ticket_no", "flight_id"),
        Index("idx_flight_id", "flight_id")
    )


class Route(Base):
    __tablename__ = "routes"
    route_no: Mapped[str] = mapped_column(Text, primary_key=True)
    validity: Mapped[str] = mapped_column(TSTZRANGE, primary_key=True)
    departure_airport: Mapped[str] = mapped_column(ForeignKey("airplane_datas.departure_airport"), nullable=False)
    arrival_airport: Mapped[str] = mapped_column(ForeignKey("airplane_datas.arrival_airport"), nullable=False)
    airplane_code: Mapped[str] = mapped_column(ForeignKey("airplane_datas.airplane_code"), nullable=False)
    days_of_week: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(Time, nullable=False)
    duration: Mapped[str] = mapped_column(Interval, nullable=False)

    __table_args__ = (
        Index("idx_departure_airport_validity", "departure_airport", text("lower(validity)")),
        ExcludeConstraint(("route_no", "="), ("validity", "&&"), name="routes_route_no_validity_excl",
                          using="gist",
                          )
    )
