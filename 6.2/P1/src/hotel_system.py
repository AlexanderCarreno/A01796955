"""Hotel Management System - Classes for Hotel, Customer, and Reservation."""

from datetime import datetime
from typing import Optional, Dict, Any
from abc import ABC, abstractmethod


class BaseEntity(ABC):
    """Abstract base class for entities."""

    @abstractmethod
    def to_dict(self) -> Dict[str, Any]:
        """Convert entity to dictionary."""
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate entity data."""
        pass


class Hotel(BaseEntity):
    """Hotel class representing a hotel with rooms and reservations."""

    def __init__(self, hotel_id: str, name: str, location: str,
                 total_rooms: int, rooms_available: int = None,
                 price_per_room: float = 0.0):
        self.hotel_id = hotel_id
        self.name = name
        self.location = location
        self.total_rooms = total_rooms
        self.rooms_available = rooms_available if rooms_available is not None else total_rooms
        self.price_per_room = price_per_room
        self.created_date = datetime.now().isoformat()

    def validate(self) -> bool:
        if not self.hotel_id or not isinstance(self.hotel_id, str):
            return False
        if not self.name or not isinstance(self.name, str):
            return False
        if not self.location or not isinstance(self.location, str):
            return False
        if not isinstance(self.total_rooms, int) or self.total_rooms <= 0:
            return False
        if not isinstance(self.rooms_available, int) or self.rooms_available < 0:
            return False
        if self.rooms_available > self.total_rooms:
            return False
        if not isinstance(self.price_per_room, (int, float)) or self.price_per_room < 0:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
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
        if self.rooms_available > 0:
            self.rooms_available -= 1
            return True
        return False

    def cancel_reservation(self) -> bool:
        if self.rooms_available < self.total_rooms:
            self.rooms_available += 1
            return True
        return False

    def __str__(self) -> str:
        return (f"Hotel(ID: {self.hotel_id}, Name: {self.name}, "
                f"Location: {self.location}, "
                f"Rooms: {self.rooms_available}/{self.total_rooms}, "
                f"Price: ${self.price_per_room})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Hotel):
            return False
        return self.hotel_id == other.hotel_id


class Customer(BaseEntity):
    def __init__(self, customer_id: str, name: str, email: str, phone: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.created_date = datetime.now().isoformat()

    def validate(self) -> bool:
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
        return {
            'customer_id': self.customer_id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'created_date': self.created_date,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Customer':
        return cls(
            customer_id=data['customer_id'],
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
        )

    def update(self, name: Optional[str] = None,
               email: Optional[str] = None,
               phone: Optional[str] = None) -> bool:
        if name is not None:
            self.name = name
        if email is not None:
            self.email = email
        if phone is not None:
            self.phone = phone
        return self.validate()

    def __str__(self) -> str:
        return (f"Customer(ID: {self.customer_id}, Name: {self.name}, "
                f"Email: {self.email}, Phone: {self.phone})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Customer):
            return False
        return self.customer_id == other.customer_id


class Reservation(BaseEntity):
    def __init__(self, reservation_id: str, customer_id: str,
                 hotel_id: str, check_in: str, check_out: str,
                 status: str = "active"):
        self.reservation_id = reservation_id
        self.customer_id = customer_id
        self.hotel_id = hotel_id
        self.check_in = check_in
        self.check_out = check_out
        self.status = status
        self.created_date = datetime.now().isoformat()

    def validate(self) -> bool:
        if not self.reservation_id or not isinstance(self.reservation_id, str):
            return False
        if not self.customer_id or not isinstance(self.customer_id, str):
            return False
        if not self.hotel_id or not isinstance(self.hotel_id, str):
            return False
        if not self.check_in or not isinstance(self.check_in, str):
            return False
        if not self.check_out or not isinstance(self.check_out, str):
            return False
        if self.status not in ["active", "cancelled"]:
            return False
        try:
            check_in_date = datetime.fromisoformat(self.check_in)
            check_out_date = datetime.fromisoformat(self.check_out)
            if check_in_date >= check_out_date:
                return False
        except ValueError:
            return False
        return True

    def to_dict(self) -> Dict[str, Any]:
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
        return cls(
            reservation_id=data['reservation_id'],
            customer_id=data['customer_id'],
            hotel_id=data['hotel_id'],
            check_in=data['check_in'],
            check_out=data['check_out'],
            status=data.get('status', 'active'),
        )

    def cancel(self) -> bool:
        if self.status == "active":
            self.status = "cancelled"
            return True
        return False

    def __str__(self) -> str:
        return (f"Reservation(ID: {self.reservation_id}, "
                f"Customer: {self.customer_id}, Hotel: {self.hotel_id}, "
                f"Check-in: {self.check_in}, Check-out: {self.check_out}, "
                f"Status: {self.status})")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Reservation):
            return False
        return self.reservation_id == other.reservation_id
