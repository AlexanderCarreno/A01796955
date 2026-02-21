"""
Hotel Management System - Software Testing and Quality Assurance Project

This project implements a complete hotel management system in Python with a focus
on software quality, testing, and compliance with industry standards.
"""

# Hotel Management System

## Overview

This is a comprehensive Hotel Management System built in Python that demonstrates
professional software engineering practices including:

- Object-oriented design with abstract base classes
- Persistent data storage using JSON files
- Comprehensive unit testing with unittest module
- Error handling and validation
- compliance with PEP8

## Project Structure

```
6.2/P1/
├── hotel_system.py              # Compatibility wrapper (imports from src/)
├── persistence.py               # Compatibility wrapper (imports from src/)
├── test_hotel_system.py         # Compatibility wrapper (imports from tests/)
├── main.py                      # Compatibility wrapper (imports from src/)
├── run_tests.py                 # Test runner wrapper
├── src/                         # Source package (canonical location)
│   ├── __init__.py
│   ├── hotel_system.py          # Hotel, Customer, Reservation classes
│   ├── persistence.py           # DataPersistence class
│   └── main.py                  # Demo implementation
├── tests/                       # Test package
│   ├── __init__.py
│   ├── test_hotel_system.py     # Unit tests
│   └── run_tests.py             # Test runner implementation
└── output/                      # Data directory (created at runtime)
    ├── hotels.json
    ├── customers.json
    └── reservations.json
```

## Requirements Satisfaction

### Classes and Abstractions
✓ **Hotel** - Represents a hotel with rooms and pricing information
✓ **Customer** - Represents a customer with contact details
✓ **Reservation** - Represents a booking linking customers to hotels
✓ **BaseEntity** - Abstract base class defining common interface

### Persistent Behaviors

#### Hotel Operations
- ✓ Create Hotel
- ✓ Delete Hotel
- ✓ Display Hotel information
- ✓ Modify Hotel Information
- ✓ Reserve a Room
- ✓ Cancel a Reservation

#### Customer Operations
- ✓ Create Customer
- ✓ Delete Customer
- ✓ Display Customer Information
- ✓ Modify Customer Information

#### Reservation Operations
- ✓ Create Reservation (Customer + Hotel)
- ✓ Cancel Reservation

### Unit Testing
✓ **81 comprehensive unit tests** using Python's unittest module
✓ Tests cover:
  - Class creation and initialization
  - Data validation
  - CRUD operations
  - Error conditions
  - Edge cases
  - Persistence layer

### Error Handling
✓ **Invalid data handling:**
  - Input validation before persistence
  - Try-catch blocks for file I/O errors
  - Error messages displayed to console
  - Execution continues after errors
  - Examples in main.py demonstration

### PEP8 Compliance
✓ Code follows PEP8 style guide:
  - Proper indentation (4 spaces)
  - Meaningful variable names
  - Docstrings for all modules and functions
  - Type hints throughout
  - Line length ≤ 79 characters (with exceptions for long strings)
  - Proper spacing and formatting

## Class Attributes

### Hotel Class
- `hotel_id` (str): Unique identifier
- `name` (str): Hotel name
- `location` (str): Hotel location
- `total_rooms` (int): Total number of rooms
- `rooms_available` (int): Currently available rooms
- `price_per_room` (float): Price per room per night
- `created_date` (str): Creation timestamp (ISO format)

### Customer Class
- `customer_id` (str): Unique identifier
- `name` (str): Customer name
- `email` (str): Email address
- `phone` (str): Phone number
- `created_date` (str): Creation timestamp (ISO format)

### Reservation Class
- `reservation_id` (str): Unique identifier
- `customer_id` (str): Associated customer ID
- `hotel_id` (str): Associated hotel ID
- `check_in` (str): Check-in date (YYYY-MM-DD)
- `check_out` (str): Check-out date (YYYY-MM-DD)
- `status` (str): "active" or "cancelled"
- `created_date` (str): Creation timestamp (ISO format)

## Usage

### Execution Instructions for Windows

#### Prerequisites
- Python 3.7 or later must be installed
- Verify Python is installed by opening Command Prompt (cmd) or PowerShell and running:
  ```cmd
  python --version
  ```

#### Step 1: Navigate to the Project Directory

Open Command Prompt or PowerShell and navigate to the project folder:

```cmd
cd D:\Documentos\Tec de Monterrey\2026 Trimestre Enero Abril\Pruebas de software y aseguramiento de la calidad\actividad_4.2._ejercicio_de_programacion_1\6.2\P1
```

Or if you're on a different drive, you may need to change drives first:

```cmd
D:
cd \Documentos\Tec de Monterrey\2026 Trimestre Enero Abril\Pruebas de software y aseguramiento de la calidad\actividad_4.2._ejercicio_de_programacion_1\6.2\P1
```

#### Step 2: Running the Demonstration

To run the main demonstration program:

```cmd
python main.py
```

**Expected Output:**
- Displays demonstrations of hotel, customer, and reservation management
- Shows successful operations and error handling examples
- Creates JSON files in the `output/` directory
- Should complete with message: `DEMONSTRATION COMPLETED SUCCESSFULLY`

#### Step 3: Running the Test Suite

##### Option A: Run tests using the test runner script
```cmd
python -m tests.run_tests
```

##### Option B: Run tests directly using unittest discovery
```cmd
python -m unittest discover -s tests -p "test_*.py" -v
```

##### Option C: Run from the root wrapper (if in project root)
```cmd
python run_tests.py
```

**Expected Output:**
- Displays all tests with PASS/FAIL status
- Summary shows: "X passed, 0 failures, 0 errors"
- Test completion time

#### Complete Example Session (Windows CMD)

```cmd
REM Navigate to project
cd D:\Documentos\Tec de Monterrey\2026 Trimestre Enero Abril\Pruebas de software y aseguramiento de la calidad\actividad_4.2._ejercicio_de_programacion_1\6.2\P1

REM Run the demonstration
python main.py

REM Run the tests
python -m tests.run_tests
```

#### Using PowerShell Alternative

If you prefer PowerShell, use the same commands:

```powershell
# Navigate to project
cd 'D:\Documentos\Tec de Monterrey\2026 Trimestre Enero Abril\Pruebas de software y aseguramiento de la calidad\actividad_4.2._ejercicio_de_programacion_1\6.2\P1'

# Run the demonstration
python main.py

# Run the tests
python -m tests.run_tests
```

#### Troubleshooting on Windows

**Issue: "python: command not found"**
- Solution: Python is not in PATH. Either:
  - Reinstall Python and check "Add Python to PATH" during installation
  - Use `py` instead: `py main.py` or `py -m tests.run_tests`

**Issue: "No module named 'src'" or "No module named 'tests'"**
- Solution: Make sure you're running commands from the `6.2\P1\` directory, not from a subdirectory

**Issue: Output folder permission denied**
- Solution: Run Command Prompt as Administrator or check folder permissions

**Issue: JSON files not created in output/ folder**
- Solution: The `output/` folder is created automatically on first run. Verify it exists after running `python main.py`

#### Data Persistence Location

After running `python main.py`, JSON files will be created in:
```
6.2\P1\output\
├── hotels.json
├── customers.json
└── reservations.json
```

View the files in File Explorer or with:
```cmd
dir output
type output\hotels.json
```

### Running Tests
```bash
# Run all tests
python -m unittest test_hotel_system -v

# Run tests with runner script
python run_tests.py
```

### Running the Demonstration

The main demonstration has been moved to the src package. Execute it using:

```cmd
python main.py
```

This will execute demonstrations of:
- Hotel management (create, retrieve, modify, reserve)
- Customer management (create, retrieve, modify)
- Reservation management (create, cancel)
- Error handling (invalid data detection)

### Using the System Programmatically
```python
from hotel_system import Hotel, Customer, Reservation
from persistence import DataPersistence

# Initialize persistence layer
persistence = DataPersistence("data")

# Create a hotel
hotel = Hotel("H001", "Grand Hotel", "New York", 100, 100, 150.0)
persistence.create_hotel(hotel)

# Create a customer
customer = Customer("C001", "John Doe", "john@example.com", "555-1234")
persistence.create_customer(customer)

# Create a reservation
reservation = Reservation("R001", "C001", "H001", "2026-03-01", "2026-03-05")
persistence.create_reservation(reservation)

# Retrieve and modify
hotel = persistence.get_hotel("H001")
if hotel:
    hotel.update(price_per_room=175.0)
    persistence.update_hotel("H001", hotel)

# Cancel reservation
reservation = persistence.get_reservation("R001")
if reservation:
    reservation.cancel()
    persistence.update_reservation("R001", reservation)
```

## Validation Rules

### Hotel Validation
- hotel_id must be a non-empty string
- name must be a non-empty string
- location must be a non-empty string
- total_rooms must be a positive integer

### Customer Validation
- customer_id must be a non-empty string
- name must be a non-empty string
- email must contain '@' symbol
- phone must be a non-empty string

### Reservation Validation
- reservation_id must be a non-empty string
- customer_id must be a non-empty string
- status must be either "active" or "cancelled"

## Test Coverage

The test suite includes:

### Hotel Tests
- Creation and initialization
- Validation (valid and invalid cases)
- Dictionary conversion
- Updating fields
- Room reservation and cancellation
- String representation and equality

### Customer Tests
- Creation and initialization
- Validation (valid and invalid cases)
- Dictionary conversion
- Updating information
- String representation and equality

### Reservation Tests
- Creation and initialization
- Validation (valid and invalid cases, date validation)
- Dictionary conversion
- Cancellation logic
- String representation and equality

### Persistence Tests
- Create, Read, Update, Delete operations
- Duplicate prevention
- Invalid data handling
- Query operations (by hotel, by customer)
- Data clearing
- Error scenarios

## Example Output

Running `python main.py`:

```
======================================================================
  HOTEL MANAGEMENT SYSTEM - DEMONSTRATION
======================================================================

======================================================================
  Hotel Management Demo
======================================================================

1. Creating hotels...
✓ Created: Hotel(ID: H001, Name: Grand Plaza Hotel, Location: New York, 
  Rooms: 100/100, Price: $150.0)
✓ Created: Hotel(ID: H002, Name: Beach Resort, Location: Miami, Rooms: 50/50, 
  Price: $200.0)

...

======================================================================
  DEMONSTRATION COMPLETED SUCCESSFULLY
======================================================================
```
