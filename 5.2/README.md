# Sales Computation Program

## Overview

This project implements a command-line Python program named `computeSales.py` that calculates the total cost of all sales recorded in a JSON file using a product price catalogue provided in another JSON file.

The program is designed to:

- Be invoked from the command line
- Handle large datasets (hundreds to thousands of records)
- Gracefully handle invalid or malformed data
- Produce human-readable output
- Measure and report execution time
- Follow PEP8 coding standards

---

## Requirements Covered

### Req 1
The program is invoked from the command line and receives two JSON files as parameters:
1. `priceCatalogue.json`
2. `salesRecord.json`

### Req 2
The program:
- Computes total cost of all sales
- Uses product prices from the catalogue file
- Prints results on screen
- Writes results to `SalesResults.txt`
- Produces human-readable formatted output

### Req 3
Invalid data is handled using:
- Try/except blocks
- Warning messages displayed in console
- Execution continues even if errors are found

### Req 4
Program name:

```bash
python computeSales.py priceCatalogue.json salesRecord.json
```

### Req 6

- The program supports large files efficiently by:
- Using dictionary lookups for O(1) price access
- Single-pass processing of sales records
- Avoiding unnecessary nested loops

### Req 7
- Execution time is measured and displayed:
- Printed on screen
- Included in SalesResults.txt

### Req 8
- The script is compliant with PEP8.

## How It Works

1. Load both JSON files.
2. Build a dictionary mapping product titles to prices.
3. Iterate over all sales records.
4. Validate:
    - Product exists
    - Quantity is valid
    - Price is valid
5. Compute item totals.
6. Accumulate total cost.
7. Record warnings for invalid entries.
8. Measure execution time.
9. Print formatted results.
10. Save results to SalesResults.txt


## Output Example
```bash
======================================================================
SALES COMPUTATION RESULTS
======================================================================

SALES DETAILS:
----------------------------------------------------------------------
Sale ID      Date         Product                        Qty      Unit Price   Total       
----------------------------------------------------------------------
1            01/12/23     Rustic breakfast               1.00     $21.32       $21.32      
1            01/12/23     Sandwich with salad            2.00     $22.48       $44.96      
1            01/12/23     Raw legums                     1.00     $17.11       $17.11      
----------------------------------------------------------------------

TOTAL SALES COST: $83.39

Execution Time: 0.0010 seconds
======================================================================
```

## Error Handling Strategy

Instead, it:
- Prints warnings to the console
- Skips invalid records
- Counts the number of errors
- Continues execution

Examples of handled errors:
- Missing fields
- Invalid JSON
- Non-numeric prices
- Non-numeric quantities
- Missing products in catalogue

## Compliance
- PEP8 compliant
- Modular functions
- Docstrings included
- Defensive programming practices applied


## How to Run
```bash
python .\5.2\P1\source\computeSales.py .\5.2\P1\tests\TC1\TC1.ProductList.json .\5.2\P1\tests\TC1\TC1.Sales.json
```