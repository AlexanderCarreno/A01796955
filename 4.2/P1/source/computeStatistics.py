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
    """Object that stores numbers and computes descriptive statistics.

    The object is initialized with the list of numbers and exposes methods
    to compute mean, median, mode, variance and standard deviation. A
    convenience method `compute_all()` runs computations in the correct order
    and stores results as attributes on the instance.
    """

    def __init__(self, numbers):
        """Initialize with the list of numbers.

        Args:
            numbers (list): List of numeric values
        """
        self.numbers = numbers
        self.mean = None
        self.median = None
        self.modes = None
        self.variance = None
        self.std_dev = None

    def calculate_mean(self):
        """Calculate and store the mean (average)."""
        self.mean = sum(self.numbers) / len(self.numbers)
        return self.mean

    def calculate_median(self):
        """Calculate and store the median."""
        sorted_nums = sorted(self.numbers)
        n = len(sorted_nums)
        if n % 2 == 1:
            self.median = sorted_nums[n // 2]
        else:
            self.median = (sorted_nums[n // 2 - 1] + sorted_nums[n // 2]) / 2
        return self.median

    def calculate_mode(self):
        """Calculate and store the mode(s). Returns 'NA' if none."""
        frequency_dict = {}
        for num in self.numbers:
            frequency_dict[num] = frequency_dict.get(num, 0) + 1

        max_frequency = max(frequency_dict.values())
        modes = [num for num, freq in frequency_dict.items() if freq == max_frequency]

        # If every value has the same frequency, there is no mode
        if len(modes) == len(frequency_dict):
            self.modes = "NA"
        else:
            # Match previous behavior: return only the first mode in a list
            self.modes = [modes[0]]

        return self.modes

    def calculate_variance(self):
        """Calculate and store the (sample) variance."""
        # recompute mean to be safe
        self.mean = sum(self.numbers) / len(self.numbers)
        squared_diffs = [(x - self.mean) ** 2 for x in self.numbers]
        # sample variance (n-1)
        self.variance = sum(squared_diffs) / (len(self.numbers) - 1)
        return self.variance

    def calculate_std_deviation(self):
        """Calculate and store the standard deviation from variance."""
        if self.variance is None:
            self.calculate_variance()
        self.std_dev = self.variance ** 0.5
        return self.std_dev

    def compute_all(self):
        """Compute mean, median, mode, variance and std deviation in order."""
        self.calculate_mean()
        self.calculate_median()
        self.calculate_mode()
        self.calculate_variance()
        self.calculate_std_deviation()
        return self


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

    # Create statistics data object and compute all stats
    stats_data = StatisticsData(numbers)
    stats_data.compute_all()

    # Calculate execution time
    end_time = time.time()
    elapsed_time = end_time - start_time

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
