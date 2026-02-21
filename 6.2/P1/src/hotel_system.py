"""Hotel Management System - Classes for Hotel, Customer, and Reservation."""

from datetime import datetime
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Abstract base class for entities."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""

    @abstractmethod
    def validate(self) -> bool:
        """Validate entity data."""


class Hotel(BaseEntity):
    """Hotel class representing a hotel with rooms and reservations."""
    def __init__(self, # pylint: disable=too-many-arguments, too-many-positional-arguments
                 hotel_id: str,
                 name: str,
                 location: str,
                 total_rooms: int,
                 rooms_available: Optional[int] = None,
                 price_per_room: float = 0.0):
        """Initialize a Hotel instance.

        Args:
            hotel_id: Unique hotel identifier.
            name: Human-readable hotel name.
            location: Hotel location string.
            total_rooms: Total number of rooms in the hotel.
            rooms_available: Number of rooms currently available; if None,
                defaults to `total_rooms`.
            price_per_room: Nightly price per room.
        """
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.rooms_available = rooms_available if rooms_available is not None else total_rooms
        self.price_per_room = price_per_room
        self.created_date = datetime.now().isoformat()

    def _validate_string_field(self, _: str, value: Any) -> bool:
        """Validate that a field is a non-empty string."""
        return bool(value and isinstance(value, str))

    def _validate_room_counts(self) -> bool:
        """Validate room count consistency."""
        rooms_valid = (isinstance(self.total_rooms, int) and self.total_rooms > 0 and
                       isinstance(self.rooms_available, int) and self.rooms_available >= 0)
        return rooms_valid and self.rooms_available <= self.total_rooms

    def _validate_price(self) -> bool:
        """Validate price field."""
        return isinstance(self.price_per_room, (int, float)) and self.price_per_room >= 0

    def validate(self) -> bool:
        """Validate hotel data fields.

        Returns True when all required fields have acceptable types and
        values; otherwise returns False.
        """
        return (self._validate_string_field('hotel_id', self.hotel_id) and
                self._validate_string_field('name', self.name) and
                self._validate_string_field('location', self.location) and
                self._validate_room_counts() and
                self._validate_price())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Hotel to a JSON-serializable dict."""
        return {
            'hotel_id': self.hotel_id,
            'name': self.name,
            'location': self.location,
            'total_rooms': self.total_rooms,
            'rooms_available': self.rooms_available,
            'price_per_room': self.price_per_room,
            'created_date': self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hotel':
        """Create a `Hotel` instance from a dictionary (typically parsed JSON)."""
        return cls(
            hotel_id=data['hotel_id'],
            name=data['name'],
            location=data['location'],
            total_rooms=data['total_rooms'],
            rooms_available=data.get('rooms_available', data['total_rooms']),
            price_per_room=data.get('price_per_room', 0.0),
        )

    def update(self, name: Optional[str] = None,
               location: Optional[str] = None,
               total_rooms: Optional[int] = None,
               price_per_room: Optional[float] = None) -> bool:
        """Update mutable hotel fields.

        Only applies provided fields and returns the result of `validate()`
        after applying changes. When reducing `total_rooms`, the new value
        must not be less than the number of occupied rooms.
        """
        if name is not None:
            self.name = name
        if location is not None:
            self.location = location
        if total_rooms is not None:
            if total_rooms < self.total_rooms - self.rooms_available:
                return False
            rooms_diff = total_rooms - self.total_rooms
            self.total_rooms = total_rooms
            self.rooms_available += rooms_diff
        if price_per_room is not None:
            self.price_per_room = price_per_room
        return self.validate()

    def reserve_room(self) -> bool:
        """Reserve a single room if available.

        Returns True and decrements `rooms_available` on success; returns
        False when no rooms are available.
        """
        if self.rooms_available > 0:
            self.rooms_available -= 1
            return True
        return False

    def cancel_reservation(self) -> bool:
        """Release a previously reserved room.

        Returns True and increments `rooms_available` when there are fewer
        available rooms than total; returns False if all rooms are already
        available.
        """
        if self.rooms_available < self.total_rooms:
            self.rooms_available += 1
            return True
        return False

    def __str__(self) -> str:
        """Return a concise human-readable representation of the hotel."""
        return (f"Hotel(ID: {self.hotel_id}, Name: {self.name}, "
            f"Location: {self.location}, "
            f"Rooms: {self.rooms_available}/{self.total_rooms}, "
            f"Price: ${self.price_per_room})")

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on `hotel_id`."""
        if not isinstance(other, Hotel):
            return False
        return self.hotel_id == other.hotel_id


class Customer(BaseEntity):
    """Customer class representing a hotel customer."""
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        """Initialize a Customer instance.

        Args:
            customer_id: Unique customer identifier.
            name: Customer full name.
            email: Customer email address.
            phone: Customer phone number.
        """
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_date = datetime.now().isoformat()

    def validate(self) -> bool:
        """Validate customer data fields.

        Returns True when all required fields are present and valid.
        """
        if not self.customer_id or not isinstance(self.customer_id, str):
            return False
        if not self.name or not isinstance(self.name, str):
            return False
        if not self.email or not isinstance(self.email, str):
            return False
        if '@' not in self.email:
            return False
        if not self.phone or not isinstance(self.phone, str):
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Customer to a JSON-serializable dict."""
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_date': self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        """Create a `Customer` instance from a dictionary.

        This is typically used when loading from persisted JSON data.
        """
        return cls(
            customer_id=data['customer_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
        )

    def update(self, name: Optional[str] = None,
               email: Optional[str] = None,
               phone: Optional[str] = None) -> bool:
        """Update customer fields and return validation result.

        Applies only provided fields; returns result of `validate()`.
        """
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        return self.validate()

    def __str__(self) -> str:
        """Return a readable representation of the customer."""
        return (f"Customer(ID: {self.customer_id}, Name: {self.name}, "
            f"Email: {self.email}, Phone: {self.phone})")

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on `customer_id`."""
        if not isinstance(other, Customer):
            return False
        return self.customer_id == other.customer_id


class Reservation(BaseEntity):
    """Reservation class representing a hotel reservation."""
    def __init__(self, # pylint: disable=too-many-arguments, too-many-positional-arguments
                 reservation_id: str,
                 customer_id: str,
                 hotel_id: str,
                 check_in: str,
                 check_out: str,
                 status: str = "active"):
        """Initialize a Reservation instance.

        Args:
            reservation_id: Unique reservation identifier.
            customer_id: ID of the customer who made the reservation.
            hotel_id: ID of the hotel reserved.
            check_in: ISO-format check-in date string.
            check_out: ISO-format check-out date string.
            status: Reservation status ("active" or "cancelled").
        """
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.created_date = datetime.now().isoformat()

    def _validate_string_fields(self) -> bool:
        """Validate all required string fields."""
        return (bool(self.reservation_id and isinstance(self.reservation_id, str)) and
                bool(self.customer_id and isinstance(self.customer_id, str)) and
                bool(self.hotel_id and isinstance(self.hotel_id, str)) and
                bool(self.check_in and isinstance(self.check_in, str)) and
                bool(self.check_out and isinstance(self.check_out, str)))

    def _validate_dates(self) -> bool:
        """Validate date format and ordering."""
        try:
            check_in_date = datetime.fromisoformat(self.check_in)
            check_out_date = datetime.fromisoformat(self.check_out)
            return check_in_date < check_out_date
        except ValueError:
            return False

    def validate(self) -> bool:
        """Validate reservation fields and date ordering.

        Ensures required fields are strings and that `check_in` < `check_out`.
        """
        return (self._validate_string_fields() and
                self.status in ["active", "cancelled"] and
                self._validate_dates())

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the Reservation to a JSON-serializable dict."""
        return {
            'reservation_id': self.reservation_id,
            'customer_id': self.customer_id,
            'hotel_id': self.hotel_id,
            'check_in': self.check_in,
            'check_out': self.check_out,
            'status': self.status,
            'created_date': self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Reservation':
        """Create a `Reservation` instance from a dictionary.

        Used when loading reservations from persisted JSON.
        """
        return cls(
            reservation_id=data['reservation_id'],
            customer_id=data['customer_id'],
            hotel_id=data['hotel_id'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            status=data.get('status', 'active'),
        )

    def cancel(self) -> bool:
        """Mark the reservation as cancelled if it is currently active.

        Returns True when status changed; otherwise False.
        """
        if self.status == "active":
            self.status = "cancelled"
            return True
        return False

    def __str__(self) -> str:
        """Return a readable representation of the reservation."""
        return (f"Reservation(ID: {self.reservation_id}, "
            f"Customer: {self.customer_id}, Hotel: {self.hotel_id}, "
            f"Check-in: {self.check_in}, Check-out: {self.check_out}, "
            f"Status: {self.status})")

    def __eq__(self, other: object) -> bool:
        """Equality comparison based on `reservation_id`."""
        if not isinstance(other, Reservation):
            return False
        return self.reservation_id == other.reservation_id
