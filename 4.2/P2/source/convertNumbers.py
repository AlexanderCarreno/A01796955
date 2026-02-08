# pylint: disable=invalid-name
"""
Convert Numbers to Binary and Hexadecimal.

This program reads a file containing numbers and converts them to binary
and hexadecimal representations using basic algorithms (not built-in
functions for base conversion).
"""

import sys
import time


def read_numbers_from_file(filename):
    """
    Read numbers from a file, handling invalid data gracefully.

    Args:
        filename (str): Path to the file containing numbers

    Returns:
        tuple: List of valid integers and count of invalid entries
    """
    numbers = []
    invalid_count = 0

    try:
        with open(filename, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                try:
                    # Convert to integer
                    num = int(line)  
                    numbers.append(num)
                except ValueError:
                    numbers.append(line)
                    invalid_count += 1
                    print(f"Error: Line {line_num} contains invalid data: "
                          f"'{line}' (skipped)")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)

    return numbers, invalid_count


def decimal_to_binary(num):
    """
    Convert a decimal number to binary using two's complement for negative numbers.
    
    Uses 10-bit representation like Excel's DEC.A.BIN function, supporting
    negative numbers in two's complement format.

    Args:
        num (int): Decimal number to convert (positive or negative)

    Returns:
        str: Binary representation of the number
    """
    if num == 0:
        return "0"
    
    # Handle negative numbers using two's complement (10-bit representation)
    if num < 0:
        # Convert to two's complement: 2^10 + num for 10-bit representation
        # This matches Excel's DEC.A.BIN behavior
        num = 1024 + num  # 1024 = 2^10
    
    # Convert positive number to binary
    binary = ""
    temp = num
    while temp > 0:
        remainder = temp % 2
        binary = str(remainder) + binary
        temp = temp // 2

    return binary


def decimal_to_hexadecimal(num):
    """
    Convert a decimal number to hexadecimal using two's complement for negative numbers.
    
    Uses 10-digit hexadecimal representation like Excel's DEC.A.HEX function, supporting
    negative numbers in two's complement format.

    Args:
        num (int): Decimal number to convert (positive or negative)

    Returns:
        str: Hexadecimal representation of the number
    """
    if num == 0:
        return "0"

    # Handle negative numbers using two's complement (10-digit hex = 40-bit representation)
    if num < 0:
        # Convert to two's complement: 16^10 + num for 10-digit hex representation
        # This matches Excel's DEC.A.HEX behavior
        num = 1099511627776 + num  # 1099511627776 = 16^10
    
    # Convert positive number to hexadecimal
    hex_chars = "0123456789ABCDEF"
    hexadecimal = ""
    temp = num

    while temp > 0:
        remainder = temp % 16
        hexadecimal = hex_chars[remainder] + hexadecimal
        temp = temp // 16

    return hexadecimal


def process_and_display_conversions(numbers, output_file, filename):
    """
    Convert numbers and display results.

    Args:
        numbers (list): List of numbers to convert
        output_file (file object): File to write results to
        filename (str): Name of the input file

    Returns:
        None
    """
    output_file.write(f"\n\n=======================================================\n")
    output_file.write(f"======= Convert Numbers for {filename} ==========\n")
    output_file.write(f"=======================================================\n")
    output_file.write("Decimal | Binary | Hexadecimal\n")
    output_file.write("-" * 40 + "\n")
    print("Decimal | Binary | Hexadecimal")
    print("-" * 40)

    for num in numbers:
        try:
            # Try to convert to binary and hexadecimal
            binary = decimal_to_binary(num)
            hexadecimal = decimal_to_hexadecimal(num)
        except (TypeError, ValueError):
            # If conversion fails, display NA
            binary = "NA"
            hexadecimal = "NA"
        if type(num) == str:
            output_line = f"{num:>7s} | {binary:>20s} | {hexadecimal:>12s}"
        else:
            output_line = f"{num:7d} | {binary:>20s} | {hexadecimal:>12s}"
        print(output_line)
        output_file.write(output_line + "\n")


def main():
    """Main function to convert numbers to binary and hexadecimal."""
    start_time = time.time()

    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python convertNumbers.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Read numbers from file
    numbers, invalid_count = read_numbers_from_file(filename)

    if not numbers:
        print("No valid numbers found in file.")
        sys.exit(1)

    # Open output file for writing
    try:
        with open("./4.2/P2/results/ConvertionResults.txt", 'a') as output_file:
            # Process and display conversions
            process_and_display_conversions(numbers, output_file, filename)

            # Calculate and display execution time
            end_time = time.time()
            elapsed_time = end_time - start_time

            # Display statistics
            stats_line = (f"\n\nSummary:\n"
                          f"Total numbers processed: {len(numbers)}\n"
                          f"Invalid entries skipped: {invalid_count}\n"
                          f"Execution time: {elapsed_time:.4f} seconds")

            print(stats_line)
            output_file.write(stats_line)

    except IOError as e:
        print(f"Error writing to output file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
