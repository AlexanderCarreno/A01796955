# pylint: disable=invalid-name
"""
Compute Statistics Module

Este programa calcula todas las estadísticas descriptivas 
a partir de un archivo que contiene números.
Lee los datos desde un archivo, calcula la media, mediana, 
moda, varianza y desviación estándar utilizando algoritmos 
básicos, y genera los resultados tanto en consola como 
en un archivo llamado StatisticsResults.txt.

Usage:
    python computeStatistics.py fileWithData.txt
"""

import sys
import time


def read_numbers_from_file(filename):
    """
    Read numbers from a file, handling invalid data gracefully.

    Args:
        filename (str): Path to the file containing numbers

    Returns:
        list: List of valid numbers extracted from the file
    """
    numbers = []
    invalid_count = 0

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                try:
                    # Try to convert to float
                    num = float(line)
                    numbers.append(num)
                except ValueError:
                    invalid_count += 1
                    print(f"Error: Line {line_num} contains invalid data: "
                          f"'{line}' (skipped)")

    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except IOError as e:
        print(f"Error: Could not read file '{filename}': {e}")
        sys.exit(1)

    if invalid_count > 0:
        print(f"Warning: {invalid_count} invalid entries were skipped.\n")

    if not numbers:
        print("Error: No valid numbers found in the file.")
        sys.exit(1)

    return numbers


def calculate_mean(numbers):
    """
    Calculate the mean (average) of numbers.

    Args:
        numbers (list): List of numbers

    Returns:
        float: The mean value
    """
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """
    Calculate the median of numbers.

    Args:
        numbers (list): List of numbers

    Returns:
        float: The median value
    """
    # Sort numbers using bubble sort (basic algorithm)
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)

    if n % 2 == 1:
        return sorted_nums[n // 2]
    else:
        return (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2


def calculate_mode(numbers):
    """
    Calculate the mode(s) of numbers.

    Args:
        numbers (list): List of numbers

    Returns:
        list: List of mode values
    """
    # Count frequencies manually
    frequency_dict = {}
    for num in numbers:
        if num in frequency_dict:
            frequency_dict[num] += 1
        else:
            frequency_dict[num] = 1

    max_frequency = max(frequency_dict.values())
    modes = [num for num, freq in frequency_dict.items()
             if freq == max_frequency]

    return sorted(modes)


def calculate_variance(numbers, mean):
    """
    Calculate the variance of numbers.

    Args:
        numbers (list): List of numbers
        mean (float): The mean of the numbers

    Returns:
        float: The variance value
    """
    sum_squared_deviations = sum((num - mean) ** 2 for num in numbers)
    return sum_squared_deviations / len(numbers)


def calculate_std_deviation(variance):
    """
    Calculate the standard deviation from variance.

    Args:
        variance (float): The variance value

    Returns:
        float: The standard deviation value
    """
    return variance ** 0.5


def format_results(numbers, mean, median, modes, variance, std_dev):
    """
    Format the statistical results for display.

    Args:
        numbers (list): List of numbers
        mean (float): The mean value
        median (float): The median value
        modes (list): List of mode values
        variance (float): The variance value
        std_dev (float): The standard deviation value

    Returns:
        str: Formatted results string
    """
    modes_str = ', '.join(f"{mode:.2f}" for mode in modes)

    results = (
        "\n" + "=====================================" + "\n"
        "DESCRIPTIVE STATISTICS RESULTS\n"
        "=====================================" + "\n"
        f"Number of items: {len(numbers)}\n"
        f"Mean: {mean:.2f}\n"
        f"Median: {median:.2f}\n"
        f"Mode(s): {modes_str}\n"
        f"Variance: {variance:.2f}\n"
        f"Standard Deviation: {std_dev:.2f}\n"
        "=====================================" + "\n"
    )

    return results


def main():
    """Main function to the statistics calculation."""
    start_time = time.time()

    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python computeStatistics.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Read numbers from file
    numbers = read_numbers_from_file(filename)

    # Calculate statistics
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    modes = calculate_mode(numbers)
    variance = calculate_variance(numbers, mean)
    std_dev = calculate_std_deviation(variance)

    # Calculate execution time
    end_time = time.time()
    elapsed_time = end_time - start_time

    # Format results
    results = format_results(numbers, mean, median, modes, variance, std_dev)
    time_str = f"Execution time: {elapsed_time:.4f} seconds\n"

    # Display on console
    print(results)
    print(time_str)

    # Write to file
    try:
        with open('StatisticsResults.txt', 'w') as output_file:
            output_file.write(results)
            output_file.write(time_str)
        print(f"Results saved to 'StatisticsResults.txt'")
    except IOError as e:
        print(f"Error: Could not write to 'StatisticsResults.txt': {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
