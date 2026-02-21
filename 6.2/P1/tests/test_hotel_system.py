"""Unit tests for Hotel Management System."""

import unittest
import os
import shutil
import tempfile
from datetime import datetime, timedelta
from src.hotel_system import Hotel, Customer, Reservation
from src.persistence import DataPersistence


class TestHotel(unittest.TestCase):
    """Test cases for Hotel class."""

    def setUp(self):
        """Set up test fixtures."""
        self.hotel = Hotel(
            hotel_id="H001",
            name="Grand Hotel",
            location="New York",
            total_rooms=100,
            rooms_available=100,
            price_per_room=150.0
        )

    def test_hotel_creation(self):
        """Test hotel creation."""
        self.assertEqual(self.hotel.hotel_id, "H001")
        self.assertEqual(self.hotel.name, "Grand Hotel")
        self.assertEqual(self.hotel.location, "New York")
        self.assertEqual(self.hotel.total_rooms, 100)
        self.assertEqual(self.hotel.rooms_available, 100)
        self.assertEqual(self.hotel.price_per_room, 150.0)

    def test_hotel_validate_valid(self):
        """Test hotel validation with valid data."""
        self.assertTrue(self.hotel.validate())

    def test_hotel_validate_invalid_id(self):
        """Test hotel validation with invalid ID."""
        self.hotel.hotel_id = ""
        self.assertFalse(self.hotel.validate())

    def test_hotel_validate_invalid_name(self):
        """Test hotel validation with invalid name."""
        self.hotel.name = ""
        self.assertFalse(self.hotel.validate())

    def test_hotel_validate_invalid_location(self):
        """Test hotel validation with invalid location."""
        self.hotel.location = ""
        self.assertFalse(self.hotel.validate())

    def test_hotel_validate_invalid_total_rooms(self):
        """Test hotel validation with invalid total rooms."""
        self.hotel.total_rooms = -1
        self.assertFalse(self.hotel.validate())

    def test_hotel_validate_rooms_available_exceeds_total(self):
        """Test hotel validation when available rooms exceed total."""
        self.hotel.rooms_available = 150
        self.assertFalse(self.hotel.validate())

    def test_hotel_validate_invalid_price(self):
        """Test hotel validation with invalid price."""
        self.hotel.price_per_room = -10.0
        self.assertFalse(self.hotel.validate())

    def test_hotel_to_dict(self):
        """Test hotel to_dict conversion."""
        hotel_dict = self.hotel.to_dict()
        self.assertEqual(hotel_dict['hotel_id'], "H001")
        self.assertEqual(hotel_dict['name'], "Grand Hotel")
        self.assertIn('created_date', hotel_dict)

    def test_hotel_from_dict(self):
        """Test hotel from_dict creation."""
        hotel_dict = {
            'hotel_id': 'H002',
            'name': 'Hotel Paradise',
            'location': 'Miami',
            'total_rooms': 50,
            'rooms_available': 45,
            'price_per_room': 200.0
        }
        hotel = Hotel.from_dict(hotel_dict)
        self.assertEqual(hotel.hotel_id, 'H002')
        self.assertEqual(hotel.name, 'Hotel Paradise')

    def test_hotel_update_name(self):
        """Test updating hotel name."""
        result = self.hotel.update(name="Updated Grand Hotel")
        self.assertTrue(result)
        self.assertEqual(self.hotel.name, "Updated Grand Hotel")

    def test_hotel_update_location(self):
        """Test updating hotel location."""
        result = self.hotel.update(location="Los Angeles")
        self.assertTrue(result)
        self.assertEqual(self.hotel.location, "Los Angeles")

    def test_hotel_update_price(self):
        """Test updating hotel price."""
        result = self.hotel.update(price_per_room=175.0)
        self.assertTrue(result)
        self.assertEqual(self.hotel.price_per_room, 175.0)

    def test_hotel_update_total_rooms_valid(self):
        """Test updating hotel total rooms with valid data."""
        self.hotel.rooms_available = 50
        result = self.hotel.update(total_rooms=120)
        self.assertTrue(result)
        self.assertEqual(self.hotel.total_rooms, 120)
        self.assertEqual(self.hotel.rooms_available, 70)

    def test_hotel_update_total_rooms_invalid(self):
        """Test updating hotel total rooms to less than occupied."""
        self.hotel.rooms_available = 50
        result = self.hotel.update(total_rooms=40)
        self.assertFalse(result)

    def test_hotel_reserve_room_success(self):
        """Test successful room reservation."""
        initial_available = self.hotel.rooms_available
        result = self.hotel.reserve_room()
        self.assertTrue(result)
        self.assertEqual(self.hotel.rooms_available, initial_available - 1)

    def test_hotel_reserve_room_no_available(self):
        """Test room reservation when no rooms available."""
        self.hotel.rooms_available = 0
        result = self.hotel.reserve_room()
        self.assertFalse(result)

    def test_hotel_cancel_reservation_success(self):
        """Test successful reservation cancellation."""
        self.hotel.rooms_available = 50
        initial_available = self.hotel.rooms_available
        result = self.hotel.cancel_reservation()
        self.assertTrue(result)
        self.assertEqual(self.hotel.rooms_available, initial_available + 1)

    def test_hotel_cancel_reservation_all_available(self):
        """Test cancellation when all rooms are available."""
        self.hotel.rooms_available = self.hotel.total_rooms
        result = self.hotel.cancel_reservation()
        self.assertFalse(result)

    def test_hotel_equality(self):
        """Test hotel equality."""
        hotel2 = Hotel("H001", "Different Name", "Different Location", 50)
        self.assertEqual(self.hotel, hotel2)

    def test_hotel_inequality(self):
        """Test hotel inequality."""
        hotel2 = Hotel("H002", "Grand Hotel", "New York", 100)
        self.assertNotEqual(self.hotel, hotel2)

    def test_hotel_str(self):
        """Test hotel string representation."""
        str_repr = str(self.hotel)
        self.assertIn("H001", str_repr)
        self.assertIn("Grand Hotel", str_repr)

