# pylint: disable=invalid-name
"""
Compute total sales cost from price catalogue and sales records.

This program reads a price catalogue in JSON format and computes the total
cost of all sales by matching products and calculating quantity-based totals.
"""

import sys
import json
import time
from pathlib import Path


def load_json_file(file_path):
    """
    Load and parse a JSON file.

    Args:
        file_path (str): Path to the JSON file to load.

    Returns:
        list: Parsed JSON content as a list of dictionaries.

    Raises:
        FileNotFoundError: If the file does not exist.
        json.JSONDecodeError: If the file is not valid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        return None


def build_price_catalogue(catalogue_data):
    """
    Build a dictionary mapping product titles to prices.

    Args:
        catalogue_data (list): List of product dictionaries from JSON.

    Returns:
        dict: Dictionary mapping product title to price.
    """
    price_map = {}
    if not catalogue_data:
        return price_map

    for idx, product in enumerate(catalogue_data):
        try:
            if not isinstance(product, dict):
                print(f"Warning: Product at index {idx} is not a dictionary.")
                continue

            title = product.get('title')
            price = product.get('price')

            if title is None:
                print(f"Warning: Product at index {idx} has no 'title' field.")
                continue

            if price is None:
                print(f"Warning: Product '{title}' has no 'price' field.")
                continue

            try:
                price_value = float(price)
                price_map[title] = price_value
            except (ValueError, TypeError):
                print(f"Warning: Invalid price '{price}' for product '{title}'.")
                continue

        except Exception as e:
            print(f"Warning: Error processing product at index {idx}: {e}")
            continue

    return price_map


def compute_sales_total(sales_data, price_map):
    """
    Compute the total cost of all sales.

    Args:
        sales_data (list): List of sale dictionaries from JSON.
        price_map (dict): Dictionary mapping product titles to prices.

    Returns:
        tuple: (total_cost, sales_details_list, error_count)
    """
    total_cost = 0.0
    sales_details = []
    error_count = 0

    if not sales_data:
        return total_cost, sales_details, error_count

    for idx, sale in enumerate(sales_data):
        try:
            if not isinstance(sale, dict):
                print(f"Warning: Sale at index {idx} is not a dictionary.")
                error_count += 1
                continue

            product = sale.get('Product')
            quantity = sale.get('Quantity')
            sale_id = sale.get('SALE_ID', 'Unknown')
            sale_date = sale.get('SALE_Date', 'Unknown')

            if product is None:
                print(f"Warning: Sale at index {idx} has no 'Product' field.")
                error_count += 1
                continue

            if quantity is None:
                print(f"Warning: Sale {sale_id} for product '{product}' "
                      f"has no 'Quantity' field.")
                error_count += 1
                continue

            if product not in price_map:
                print(f"Warning: Product '{product}' (Sale {sale_id}, "
                      f"Date {sale_date}) not found in price catalogue.")
                error_count += 1
                continue

            try:
                qty_value = float(quantity)
                if qty_value < 0:
                    print(f"Warning: Negative quantity {qty_value} for "
                          f"product '{product}' (Sale {sale_id}).")
                    error_count += 1
                    continue

                price = price_map[product]
                item_cost = price * qty_value
                total_cost += item_cost

                sales_details.append({
                    'sale_id': sale_id,
                    'date': sale_date,
                    'product': product,
                    'quantity': qty_value,
                    'unit_price': price,
                    'total': item_cost
                })

            except (ValueError, TypeError):
                print(f"Warning: Invalid quantity '{quantity}' for product "
                      f"'{product}' (Sale {sale_id}).")
                error_count += 1
                continue

        except Exception as e:
            print(f"Warning: Error processing sale at index {idx}: {e}")
            error_count += 1
            continue

    return total_cost, sales_details, error_count


def format_results(total_cost, sales_details, execution_time, error_count):
    """
    Format results as a human-readable string.

    Args:
        total_cost (float): Total cost of all sales.
        sales_details (list): List of detailed sale information.
        execution_time (float): Time elapsed for execution in seconds.
        error_count (int): Number of errors encountered.

    Returns:
        str: Formatted results string.
    """
    lines = []
    lines.append("=" * 70)
    lines.append("SALES COMPUTATION RESULTS")
    lines.append("=" * 70)
    lines.append("")

    lines.append("SALES DETAILS:")
    lines.append("-" * 70)
    lines.append(f"{'Sale ID':<12} {'Date':<12} {'Product':<30} "
                 f"{'Qty':<8} {'Unit Price':<12} {'Total':<12}")
    lines.append("-" * 70)

    for sale in sales_details:
        lines.append(f"{str(sale['sale_id']):<12} {str(sale['date']):<12} "
                     f"{sale['product']:<30} {sale['quantity']:<8.2f} "
                     f"${sale['unit_price']:<11.2f} ${sale['total']:<11.2f}")

    lines.append("-" * 70)
    lines.append("")
    lines.append(f"TOTAL SALES COST: ${total_cost:,.2f}")
    lines.append("")

    if error_count > 0:
        lines.append(f"Warnings/Errors Encountered: {error_count}")
        lines.append("")

    lines.append(f"Execution Time: {execution_time:.4f} seconds")
    lines.append("=" * 70)

    return "\n".join(lines)


def main():
    """Main function to compute sales."""
    start_time = time.time()

    # Validate command line arguments
    if len(sys.argv) != 3:
        print("Usage: python computeSales.py priceCatalogue.json "
              "salesRecord.json")
        sys.exit(1)

    price_catalogue_file = sys.argv[1]
    sales_record_file = sys.argv[2]

    # Load JSON files
    print("Loading files...")
    catalogue_data = load_json_file(price_catalogue_file)
    if catalogue_data is None:
        sys.exit(1)

    sales_data = load_json_file(sales_record_file)
    if sales_data is None:
        sys.exit(1)

    print("Building price catalogue...")
    price_map = build_price_catalogue(catalogue_data)

    if not price_map:
        print("Error: Price catalogue is empty.")
        sys.exit(1)

    print("Computing sales...")
    total_cost, sales_details, error_count = compute_sales_total(
        sales_data, price_map
    )

    # Calculate execution time
    execution_time = time.time() - start_time

    # Format results
    results = format_results(total_cost, sales_details, execution_time,
                             error_count)

    # Display results to console
    print("")
    print(results)

    # Write results to file
    output_file = Path('./5.2/P1/results/SalesResults.txt')
    try:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'a', encoding='utf-8') as f:
            f.write(results)
        print(f"\nResults saved to '{output_file}'")
    except IOError as e:
        print(f"Error: Could not write to '{output_file}': {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
