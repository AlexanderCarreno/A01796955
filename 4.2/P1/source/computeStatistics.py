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


class StatisticsData:
    """Data class to hold statistics calculation parameters."""

    def __init__(self, numbers, mean, median, modes, variance, std_dev):
        """Initialize statistics data.

        Args:
            numbers (list): List of numbers
            mean (float): The mean value
            median (float): The median value
            modes (list): List of mode values
            variance (float): The variance value
            std_dev (float): The standard deviation value
        """
        self.numbers = numbers
        self.mean = mean
        self.median = median
        self.modes = modes
        self.variance = variance
        self.std_dev = std_dev


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
        median = sorted_nums[n // 2]
    else:
        median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2

    return median


def calculate_mode(numbers):
    """
    Simula la función MODA de Excel.
    Devuelve la primera moda encontrada en la lista.
    
    Args:
        numbers (list): Lista de números

    Returns:
        int/float/str: La moda encontrada, o "NA" si no existe
    """
    # Contar frecuencias
    frequency_dict = {}
    for num in numbers:
        frequency_dict[num] = frequency_dict.get(num, 0) + 1

    max_frequency = max(frequency_dict.values())
    modes = [num for num, freq in frequency_dict.items()
             if freq == max_frequency]

    # Si todos los números tienen la misma frecuencia → no hay moda
    if len(modes) == len(frequency_dict):
        return "NA"

    # Devolver solo la primera moda encontrada (como hace Excel MODA)
    return [modes[0]]


def calculate_variance(numbers, mean):
    """
    Calculate the variance of numbers.

    Args:
        numbers (list): List of numbers
        mean (float): The mean of the numbers

    Returns:
        float: The variance value
    """
    mean = sum(numbers) / len(numbers)
    squared_diffs = [(x - mean) ** 2 for x in numbers]
    return sum(squared_diffs) / (len(numbers) - 1)


def calculate_std_deviation(variance):
    """
    Calculate the standard deviation from variance.

    Args:
        variance (float): The variance value

    Returns:
        float: The standard deviation value
    """
    return variance ** 0.5


def format_results(filename, stats_data):
    """
    Format the statistical results for display.

    Args:
        filename (str): The name of the input file
        stats_data (StatisticsData): Object containing all statistics data

    Returns:
        str: Formatted results string
    """
    # check if modes is "NA" or a list of numbers
    if stats_data.modes == "NA":
        modes_str = "NA"
    else:
        modes_str = ', '.join(f"{mode:.2f}" for mode in stats_data.modes)

    results = (
        "\n" + "=====================================" + "\n"
        f"DESCRIPTIVE STATISTICS RESULTS for {filename}\n"
        "=====================================" + "\n"
        f"Number of items: {len(stats_data.numbers)}\n"
        f"Mean: {stats_data.mean:.2f}\n"
        f"Median: {stats_data.median:.2f}\n"
        f"Mode(s): {modes_str}\n"
        f"Variance: {stats_data.variance:.2f}\n"
        f"Standard Deviation: {stats_data.std_dev:.2f}\n"
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

    # Create statistics data object
    stats_data = StatisticsData(numbers, mean, median, modes, variance, std_dev)

    # Format results
    results = format_results(filename, stats_data)
    time_str = f"Execution time: {elapsed_time:.4f} seconds\n"

    # Display on console
    print(results)
    print(time_str)

    # Write to file
    try:
        with open('./4.2/P1/results/StatisticsResults.txt', 'a', encoding='utf-8') as output_file:
            output_file.write(results)
            output_file.write(time_str)
        print("Results saved to '/4.2/P1/results/StatisticsResults.txt'")
    except IOError as e:
        print(f"Error: Could not write to '/4.2/P1/results/StatisticsResults.txt': {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
