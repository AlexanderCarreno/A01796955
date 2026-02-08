# pylint: disable=invalid-name
"""
wordCount.py

Identify distinct words and count their frequency.

This program reads a text file, counts the frequency of each distinct word
using basic algorithms (not built-in functions for counting or sorting),
and outputs the results to both the console and an output file.
"""
import sys
import time


def read_file_words(filename):
    """
    Read words from file and return them.

    Args:
        filename: Path to the file to read

    Returns:
        List of words from the file
    """
    words = []
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
            # Split by whitespace to get words
            words = content.split()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return []
    except IOError as e:
        print(f"Error: Unable to read file '{filename}': {e}")
        return []

    return words


def validate_word(word):
    """
    Validate if a word is valid (non-empty string).

    Args:
        word: Word to validate

    Returns:
        True if word is valid, False otherwise
    """
    if not word or not isinstance(word, str):
        return False
    return len(word.strip()) > 0


def count_word_frequencies(words):
    """
    Count frequency of each word using basic algorithm.

    Args:
        words: List of words to count

    Returns:
        Dictionary with word frequencies and list of errors
    """
    frequencies = {}
    errors = []

    for i, word in enumerate(words):
        try:
            if not validate_word(word):
                error_msg = f"Error at position {i}: Invalid word '{word}'"
                print(error_msg)
                errors.append(error_msg)
                continue

            # Convert to lowercase for case-insensitive counting
            word_lower = word.lower()

            # Check if word already exists in dictionary
            found = False
            for key in frequencies:
                if key == word_lower:
                    frequencies[key] += 1
                    found = True
                    break

            if not found:
                frequencies[word_lower] = 1

        except (TypeError, AttributeError) as e:
            error_msg = f"Error processing word at position {i}: {e}"
            print(error_msg)
            errors.append(error_msg)

    return frequencies, errors


def sort_frequencies(frequencies):
    """
    Sort frequencies by word alphabetically using basic algorithm.

    Args:
        frequencies: Dictionary of word frequencies

    Returns:
        List of tuples (word, frequency) sorted alphabetically
    """
    # Convert dictionary to list of tuples
    items = []
    for word, count in frequencies.items():
        items.append((word, count))

    # Bubble sort by word (alphabetically)
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j][0] > items[j + 1][0]:
                # Swap
                items[j], items[j + 1] = items[j + 1], items[j]

    return items


def write_results_to_file(filename, original_filename, frequencies_sorted, elapsed_time):
    """
    Write results to output file.

    Args:
        filename: Output filename
        original_filename: Original input filename
        frequencies_sorted: Sorted list of (word, frequency) tuples
        elapsed_time: Time elapsed in seconds
    """
    try:
        with open(filename, 'a', encoding='utf-8') as file:
            file.write(f"WORD COUNT RESULTS FOR FILE: {original_filename}\n")
            file.write("=" * 40 + "\n\n")

            file.write("Word Frequencies:\n")
            file.write("-" * 40 + "\n")

            for word, count in frequencies_sorted:
                file.write(f"{word}: {count}\n")

            file.write("\n" + "=" * 40 + "\n")
            file.write(f"Total unique words: {len(frequencies_sorted)}\n")
            file.write(f"Execution time: {elapsed_time:.4f} seconds\n\n")

    except IOError as e:
        print(f"Error: Unable to write results to file: {e}")


def print_results(frequencies_sorted, elapsed_time):
    """
    Print results to console.

    Args:
        frequencies_sorted: Sorted list of (word, frequency) tuples
        elapsed_time: Time elapsed in seconds
    """
    print("\n" + "=" * 40)
    print("WORD COUNT RESULTS")
    print("=" * 40 + "\n")

    print("Word Frequencies:")
    print("-" * 40)

    for word, count in frequencies_sorted:
        print(f"{word}: {count}")

    print("\n" + "=" * 40)
    print(f"Total unique words: {len(frequencies_sorted)}")
    print(f"Execution time: {elapsed_time:.4f} seconds")
    print("=" * 40 + "\n")


def main():
    """Main function to count word frequencies in a file."""
    start_time = time.time()

    # Check command line arguments
    if len(sys.argv) < 2:
        print("Usage: python wordCount.py <filename>")
        print("Example: python wordCount.py fileWithData.txt")
        sys.exit(1)

    filename = sys.argv[1]

    # Read words from file
    words = read_file_words(filename)

    if not words:
        print("No words to process.")
        sys.exit(1)

    # Count word frequencies
    frequencies, _ = count_word_frequencies(words)

    if not frequencies:
        print("No valid words found in file.")
        sys.exit(1)

    # Sort frequencies alphabetically
    frequencies_sorted = sort_frequencies(frequencies)

    # Calculate elapsed time
    elapsed_time = time.time() - start_time

    # Print results to console
    print_results(frequencies_sorted, elapsed_time)

    # Write results to file
    output_filename = "./4.2/P3/results/WordCountResults.txt"
    write_results_to_file(output_filename, filename, frequencies_sorted, elapsed_time)
    print(f"Results saved to '{output_filename}'")


if __name__ == '__main__':
    main()
