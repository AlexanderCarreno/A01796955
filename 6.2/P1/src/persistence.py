"""Persistence layer for Hotel Management System (src package)."""

import json
import os
from typing import List, Optional, Dict, Any
from hotel_system import Hotel, Customer, Reservation


class DataPersistence:
    """Handles persistent storage of hotels, customers, and reservations."""

    def __init__(self, data_dir: Optional[str] = None):
        """
        Initialize persistence layer.

        If `data_dir` is None, use the project's `output/` directory.
        """
        if data_dir is None:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
            data_dir = os.path.join(base, 'output')

        self.data_dir = data_dir
        self.hotels_file = os.path.join(self.data_dir, "hotels.json")
        self.customers_file = os.path.join(self.data_dir, "customers.json")
        self.reservations_file = os.path.join(self.data_dir, "reservations.json")

        self._ensure_directory()
        self._ensure_files()

    def _ensure_directory(self) -> None:
        """Ensure that the data directory exists, creating it if necessary."""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _ensure_files(self) -> None:
        """Create empty JSON files for hotels, customers and reservations.

        Creates files with an empty list if they do not already exist.
        """
        for file_path in [self.hotels_file, self.customers_file, self.reservations_file]:
            if not os.path.exists(file_path):
                self._write_json_file(file_path, [])

    def _read_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Read and return list data from a JSON file.

        Returns an empty list on JSON errors or if the file is missing.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {file_path}: {str(e)}")
            return []
        except (KeyError, TypeError, ValueError) as e:
            print(f"Unexpected error reading {file_path}: {str(e)}")
            return []

    def _write_json_file(self, file_path: str, data: List[Dict[str, Any]]) -> bool:
        """Write a list of dictionaries to a JSON file.

        Returns True on success, False on error.
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except (KeyError, TypeError, ValueError) as e:
            print(f"Error writing {file_path}: {str(e)}")
            return False

    # Hotel operations
    def create_hotel(self, hotel: Hotel) -> bool:
        """Persist a new hotel if it does not already exist.

        Validates the `Hotel` object, ensures the ID is unique and appends
        the serialized hotel to the hotels JSON file.
        """
        if not hotel.validate():
            print("Error: Invalid hotel data")
            return False
        hotels = self._read_json_file(self.hotels_file)
        for h in hotels:
            if h.get('hotel_id') == hotel.hotel_id:
                print(f"Error: Hotel with ID {hotel.hotel_id} already exists")
                return False
        hotels.append(hotel.to_dict())
        return self._write_json_file(self.hotels_file, hotels)

    def get_hotel(self, hotel_id: str) -> Optional[Hotel]:
        """Retrieve a `Hotel` by its `hotel_id` or return None if not found."""
        hotels = self._read_json_file(self.hotels_file)
        for hotel_data in hotels:
            if hotel_data.get('hotel_id') == hotel_id:
                try:
                    return Hotel.from_dict(hotel_data)
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error creating Hotel from data: {str(e)}")
                    continue
        return None

    def get_all_hotels(self) -> List[Hotel]:
        """Return all valid `Hotel` instances stored in the hotels file."""
        hotels = self._read_json_file(self.hotels_file)
        hotel_list: List[Hotel] = []
        for hotel_data in hotels:
            try:
                hotel = Hotel.from_dict(hotel_data)
                if hotel.validate():
                    hotel_list.append(hotel)
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error creating Hotel from data: {str(e)}")
                continue
        return hotel_list

    def update_hotel(self, hotel_id: str, hotel: Hotel) -> bool:
        """Replace the stored hotel data for `hotel_id` with the provided
        `Hotel` instance. Returns True on success.
        """
        if not hotel.validate():
            print("Error: Invalid hotel data")
            return False
        hotels = self._read_json_file(self.hotels_file)
        for i, h in enumerate(hotels):
            if h.get('hotel_id') == hotel_id:
                hotels[i] = hotel.to_dict()
                return self._write_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel with ID {hotel_id} not found")
        return False

    def delete_hotel(self, hotel_id: str) -> bool:
        """Delete a hotel by `hotel_id`. Returns True if deletion occurred."""
        hotels = self._read_json_file(self.hotels_file)
        initial_length = len(hotels)
        hotels = [h for h in hotels if h.get('hotel_id') != hotel_id]
        if len(hotels) < initial_length:
            return self._write_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel with ID {hotel_id} not found")
        return False

    # Customer operations
    def create_customer(self, customer: Customer) -> bool:
        """Persist a new customer if the ID is unique and data validates."""
        if not customer.validate():
            print("Error: Invalid customer data")
            return False
        customers = self._read_json_file(self.customers_file)
        for c in customers:
            if c.get('customer_id') == customer.customer_id:
                print(f"Error: Customer with ID {customer.customer_id} already exists")
                return False
        customers.append(customer.to_dict())
        return self._write_json_file(self.customers_file, customers)

    def get_customer(self, customer_id: str) -> Optional[Customer]:
        """Retrieve a `Customer` by `customer_id`, or None if not found."""
        customers = self._read_json_file(self.customers_file)
        for customer_data in customers:
            if customer_data.get('customer_id') == customer_id:
                try:
                    return Customer.from_dict(customer_data)
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error creating Customer from data: {str(e)}")
                    continue
        return None

    def get_all_customers(self) -> List[Customer]:
        """Return all valid `Customer` instances stored in the customers file."""
        customers = self._read_json_file(self.customers_file)
        customer_list: List[Customer] = []
        for customer_data in customers:
            try:
                customer = Customer.from_dict(customer_data)
                if customer.validate():
                    customer_list.append(customer)
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error creating Customer from data: {str(e)}")
                continue
        return customer_list

    def update_customer(self, customer_id: str, customer: Customer) -> bool:
        """Update the stored customer data for `customer_id`.

        Returns True on success.
        """
        if not customer.validate():
            print("Error: Invalid customer data")
            return False
        customers = self._read_json_file(self.customers_file)
        for i, c in enumerate(customers):
            if c.get('customer_id') == customer_id:
                customers[i] = customer.to_dict()
                return self._write_json_file(self.customers_file, customers)
        print(f"Error: Customer with ID {customer_id} not found")
        return False

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer by `customer_id`. Returns True if deleted."""
        customers = self._read_json_file(self.customers_file)
        initial_length = len(customers)
        customers = [c for c in customers if c.get('customer_id') != customer_id]
        if len(customers) < initial_length:
            return self._write_json_file(self.customers_file, customers)
        print(f"Error: Customer with ID {customer_id} not found")
        return False

    # Reservation operations
    def create_reservation(self, reservation: Reservation) -> bool:
        """Persist a reservation if it validates and has a unique ID."""
        if not reservation.validate():
            print("Error: Invalid reservation data")
            return False
        reservations = self._read_json_file(self.reservations_file)
        for r in reservations:
            if r.get('reservation_id') == reservation.reservation_id:
                print(f"Error: Reservation with ID {reservation.reservation_id} already exists")
                return False
        reservations.append(reservation.to_dict())
        return self._write_json_file(self.reservations_file, reservations)

    def get_reservation(self, reservation_id: str) -> Optional[Reservation]:
        """Retrieve a `Reservation` by `reservation_id`, or None if not found."""
        reservations = self._read_json_file(self.reservations_file)
        for res_data in reservations:
            if res_data.get('reservation_id') == reservation_id:
                try:
                    return Reservation.from_dict(res_data)
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return None

    def get_all_reservations(self) -> List[Reservation]:
        """Return all valid `Reservation` instances stored in the reservations file."""
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            try:
                reservation = Reservation.from_dict(res_data)
                if reservation.validate():
                    res_list.append(reservation)
            except (KeyError, TypeError, ValueError) as e:
                print(f"Error creating Reservation from data: {str(e)}")
                continue
        return res_list

    def update_reservation(self, reservation_id: str, reservation: Reservation) -> bool:
        """Update a reservation record by ID. Returns True on success."""
        if not reservation.validate():
            print("Error: Invalid reservation data")
            return False
        reservations = self._read_json_file(self.reservations_file)
        for i, r in enumerate(reservations):
            if r.get('reservation_id') == reservation_id:
                reservations[i] = reservation.to_dict()
                return self._write_json_file(self.reservations_file, reservations)
        print(f"Error: Reservation with ID {reservation_id} not found")
        return False

    def delete_reservation(self, reservation_id: str) -> bool:
        """Delete a reservation by `reservation_id`. Returns True if deleted."""
        reservations = self._read_json_file(self.reservations_file)
        initial_length = len(reservations)
        reservations = [r for r in reservations if r.get('reservation_id') != reservation_id]
        if len(reservations) < initial_length:
            return self._write_json_file(self.reservations_file, reservations)
        print(f"Error: Reservation with ID {reservation_id} not found")
        return False

    def get_reservations_by_hotel(self, hotel_id: str) -> List[Reservation]:
        """Return active reservations for a specific hotel ID."""
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            if res_data.get('hotel_id') == hotel_id and res_data.get('status') == 'active':
                try:
                    reservation = Reservation.from_dict(res_data)
                    if reservation.validate():
                        res_list.append(reservation)
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return res_list

    def get_reservations_by_customer(self, customer_id: str) -> List[Reservation]:
        """Return all reservations for a given customer ID."""
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            if res_data.get('customer_id') == customer_id:
                try:
                    reservation = Reservation.from_dict(res_data)
                    if reservation.validate():
                        res_list.append(reservation)
                except (KeyError, TypeError, ValueError) as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return res_list

    def clear_all_data(self) -> bool:
        """Clear all stored hotels, customers, and reservations.

        Returns True if all files were successfully written as empty lists.
        """
        result = True
        result = self._write_json_file(self.hotels_file, []) and result
        result = self._write_json_file(self.customers_file, []) and result
        result = self._write_json_file(self.reservations_file, []) and result
        return result
