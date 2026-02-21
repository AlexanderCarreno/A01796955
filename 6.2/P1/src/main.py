"""Main entry point for Hotel Management System (src package)."""

import os
import sys

# Handle both module and direct script execution
if __name__ == '__main__':
    # When executed directly (python main.py), add parent to sys.path
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from hotel_system import Hotel, Customer, Reservation # pylint: disable=E0401
    from persistence import DataPersistence # pylint: disable=E0401
else:
    # When imported as a module, use relative imports
    from .hotel_system import Hotel, Customer, Reservation
    from .persistence import DataPersistence


def print_header(title: str) -> None:
    """Print a formatted header for demo sections.

    Args:
        title: The title text to print inside the header.
    """
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def demo_hotels(persistence: DataPersistence) -> None:
    """Run a short demonstration of hotel CRUD and listing operations.

    The function creates two example hotels, saves them using the provided
    persistence layer, retrieves one by ID, and prints all stored hotels.

    Args:
        persistence: An instance of `DataPersistence` used for storage.
    """
    print_header("Hotel Management Demo")
    h1 = Hotel("H001", "Grand Plaza Hotel", "New York", 100, 100, 150.0)
    h2 = Hotel("H002", "Beach Resort", "Miami", 50, 50, 200.0)
    persistence.create_hotel(h1)
    persistence.create_hotel(h2)
    hotel = persistence.get_hotel("H001")
    if hotel:
        print(f"✓ Retrieved: {hotel}")
    for hotel_obj in persistence.get_all_hotels():
        print(f"  - {hotel_obj}")


def demo_customers(persistence: DataPersistence) -> None:
    """Run a short demonstration of customer CRUD operations.

    The function creates two example customers, stores them via the
    provided persistence layer, and retrieves one customer by ID.

    Args:
        persistence: An instance of `DataPersistence` used for storage.
    """
    print_header("Customer Management Demo")
    c1 = Customer("C001", "John Smith", "john@example.com", "555-1001")
    c2 = Customer("C002", "Maria Garcia", "maria@example.com", "555-1002")
    persistence.create_customer(c1)
    persistence.create_customer(c2)
    customer = persistence.get_customer("C001")
    if customer:
        print(f"✓ Retrieved: {customer}")


def demo_reservations(persistence: DataPersistence) -> None:
    """Run a short demonstration of reservation creation and listing.

    The function creates two example reservations and stores them via the
    provided persistence layer, then prints all stored reservations.

    Args:
        persistence: An instance of `DataPersistence` used for storage.
    """
    print_header("Reservation Management Demo")
    r1 = Reservation("R001", "C001", "H001", "2026-03-01", "2026-03-05")
    r2 = Reservation("R002", "C002", "H002", "2026-03-10", "2026-03-15")
    persistence.create_reservation(r1)
    persistence.create_reservation(r2)
    for res_obj in persistence.get_all_reservations():
        print(f"  - {res_obj}")


def demo_error_handling() -> None:
    """Demonstrate simple validation error cases.

    This function constructs intentionally invalid entities to show how the
    validation logic reports errors (printed to stdout).
    """
    print_header("Error Handling Demo")
    invalid_customer = Customer("C999", "No Email", "invalid-email", "555-0000")
    if not invalid_customer.validate():
        print("✓ Invalid email detected - validation failed")


def main() -> None:
    """Main demonstration entry point.

    Sets up the `DataPersistence` instance (writing to the project's `output/`
    directory), clears any previous demo data, and runs the demo sections.

    If an unexpected error occurs the program exits with a non-zero status.
    """
    print("\n" + "=" * 70)
    print("  HOTEL MANAGEMENT SYSTEM - DEMONSTRATION")
    print("=" * 70)

    # Default output directory at project root
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base, 'output')
    persistence = DataPersistence(data_dir)

    try:
        persistence.clear_all_data()
        demo_hotels(persistence)
        demo_customers(persistence)
        demo_reservations(persistence)
        demo_error_handling()
        print("\n" + "=" * 70)
        print("  DEMONSTRATION COMPLETED SUCCESSFULLY")
        print("=" * 70 + "\n")
    except (KeyError, TypeError, ValueError) as e:
        print(f"\nError during demonstration: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
