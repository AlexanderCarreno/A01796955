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
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    def _ensure_files(self) -> None:
        for file_path in [self.hotels_file, self.customers_file, self.reservations_file]:
            if not os.path.exists(file_path):
                self._write_json_file(file_path, [])

    def _read_json_file(self, file_path: str) -> List[Dict[str, Any]]:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error reading {file_path}: {str(e)}")
            return []
        except Exception as e:
            print(f"Unexpected error reading {file_path}: {str(e)}")
            return []

    def _write_json_file(self, file_path: str, data: List[Dict[str, Any]]) -> bool:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error writing {file_path}: {str(e)}")
            return False

    # Hotel operations
    def create_hotel(self, hotel: Hotel) -> bool:
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
        hotels = self._read_json_file(self.hotels_file)
        for hotel_data in hotels:
            if hotel_data.get('hotel_id') == hotel_id:
                try:
                    return Hotel.from_dict(hotel_data)
                except Exception as e:
                    print(f"Error creating Hotel from data: {str(e)}")
                    continue
        return None

    def get_all_hotels(self) -> List[Hotel]:
        hotels = self._read_json_file(self.hotels_file)
        hotel_list: List[Hotel] = []
        for hotel_data in hotels:
            try:
                hotel = Hotel.from_dict(hotel_data)
                if hotel.validate():
                    hotel_list.append(hotel)
            except Exception as e:
                print(f"Error creating Hotel from data: {str(e)}")
                continue
        return hotel_list

    def update_hotel(self, hotel_id: str, hotel: Hotel) -> bool:
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
        hotels = self._read_json_file(self.hotels_file)
        initial_length = len(hotels)
        hotels = [h for h in hotels if h.get('hotel_id') != hotel_id]
        if len(hotels) < initial_length:
            return self._write_json_file(self.hotels_file, hotels)
        print(f"Error: Hotel with ID {hotel_id} not found")
        return False

    # Customer operations
    def create_customer(self, customer: Customer) -> bool:
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
        customers = self._read_json_file(self.customers_file)
        for customer_data in customers:
            if customer_data.get('customer_id') == customer_id:
                try:
                    return Customer.from_dict(customer_data)
                except Exception as e:
                    print(f"Error creating Customer from data: {str(e)}")
                    continue
        return None

    def get_all_customers(self) -> List[Customer]:
        customers = self._read_json_file(self.customers_file)
        customer_list: List[Customer] = []
        for customer_data in customers:
            try:
                customer = Customer.from_dict(customer_data)
                if customer.validate():
                    customer_list.append(customer)
            except Exception as e:
                print(f"Error creating Customer from data: {str(e)}")
                continue
        return customer_list

    def update_customer(self, customer_id: str, customer: Customer) -> bool:
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
        customers = self._read_json_file(self.customers_file)
        initial_length = len(customers)
        customers = [c for c in customers if c.get('customer_id') != customer_id]
        if len(customers) < initial_length:
            return self._write_json_file(self.customers_file, customers)
        print(f"Error: Customer with ID {customer_id} not found")
        return False

    # Reservation operations
    def create_reservation(self, reservation: Reservation) -> bool:
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
        reservations = self._read_json_file(self.reservations_file)
        for res_data in reservations:
            if res_data.get('reservation_id') == reservation_id:
                try:
                    return Reservation.from_dict(res_data)
                except Exception as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return None

    def get_all_reservations(self) -> List[Reservation]:
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            try:
                reservation = Reservation.from_dict(res_data)
                if reservation.validate():
                    res_list.append(reservation)
            except Exception as e:
                print(f"Error creating Reservation from data: {str(e)}")
                continue
        return res_list

    def update_reservation(self, reservation_id: str, reservation: Reservation) -> bool:
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
        reservations = self._read_json_file(self.reservations_file)
        initial_length = len(reservations)
        reservations = [r for r in reservations if r.get('reservation_id') != reservation_id]
        if len(reservations) < initial_length:
            return self._write_json_file(self.reservations_file, reservations)
        print(f"Error: Reservation with ID {reservation_id} not found")
        return False

    def get_reservations_by_hotel(self, hotel_id: str) -> List[Reservation]:
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            if res_data.get('hotel_id') == hotel_id and res_data.get('status') == 'active':
                try:
                    reservation = Reservation.from_dict(res_data)
                    if reservation.validate():
                        res_list.append(reservation)
                except Exception as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return res_list

    def get_reservations_by_customer(self, customer_id: str) -> List[Reservation]:
        reservations = self._read_json_file(self.reservations_file)
        res_list: List[Reservation] = []
        for res_data in reservations:
            if res_data.get('customer_id') == customer_id:
                try:
                    reservation = Reservation.from_dict(res_data)
                    if reservation.validate():
                        res_list.append(reservation)
                except Exception as e:
                    print(f"Error creating Reservation from data: {str(e)}")
                    continue
        return res_list

    def clear_all_data(self) -> bool:
        result = True
        result = self._write_json_file(self.hotels_file, []) and result
        result = self._write_json_file(self.customers_file, []) and result
        result = self._write_json_file(self.reservations_file, []) and result
        return result
