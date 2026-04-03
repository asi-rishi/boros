
import csv
import re
from datetime import datetime

def validate_transaction(transaction, processed_ids):
    """
    Validates a single transaction against a set of business rules.

    Args:
        transaction (dict): A dictionary representing a single transaction row.
        processed_ids (set): A set of transaction IDs that have already been
                                successfully processed.

    Returns:
        list: A list of error messages. An empty list means the transaction is valid.
    """
    errors = []
    today = datetime.now().date()

    # Rule 1: Transaction ID Format & Uniqueness
    tid = transaction.get('transaction_id', '')
    if not re.match(r'^TRX\d{5}$', tid):
        errors.append("Invalid Transaction ID format")
    elif tid in processed_ids:
        errors.append("Duplicate Transaction ID")

    # Rule 2: Product Name Content
    pname = transaction.get('product_name', '')
    if not pname or not pname.strip():
        errors.append("Empty/Whitespace Product Name")
    if 'spam' in pname.lower():
        errors.append("Product Name contains SPAM")

    # Rule 3: Amount & Currency Validity
    amount_str = transaction.get('amount', '')
    try:
        amount = float(amount_str)
        if amount <= 0:
            errors.append("Invalid Amount")
    except (ValueError, TypeError):
        errors.append("Invalid Amount")

    currency = transaction.get('currency', '')
    if currency not in ["USD", "EUR", "GBP", "JPY"]:
        errors.append("Invalid Currency")

    # Rule 4: Transaction Date Validity
    date_str = transaction.get('transaction_date', '')
    try:
        transaction_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        if transaction_date > today:
            errors.append("Future Date")
    except ValueError:
        errors.append("Invalid Date Format")

    return errors

def process_transactions(input_file, valid_file, rejected_file):
    """
    Reads, validates, and processes transactions from a CSV file.

    Args:
        input_file (str): Path to the input CSV file.
        valid_file (str): Path to the output CSV file for valid transactions.
        rejected_file (str): Path to the output CSV file for rejected transactions.
    """
    valid_transactions = []
    rejected_transactions = []
    processed_transaction_ids = set()
    rejection_counts = {}
    total_rows = 0

    try:
        with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            headers = reader.fieldnames

            for row in reader:
                total_rows += 1
                errors = validate_transaction(row, processed_transaction_ids)

                if not errors:
                    valid_transactions.append(row)
                    processed_transaction_ids.add(row['transaction_id'])
                else:
                    for error in errors:
                        rejection_counts[error] = rejection_counts.get(error, 0) + 1
                    row['error'] = ";".join(errors)
                    rejected_transactions.append(row)

        # Write valid transactions
        with open(valid_file, mode='w', newline='', encoding='utf-8') as outfile:
            writer = csv.DictWriter(outfile, fieldnames=headers)
            writer.writeheader()
            writer.writerows(valid_transactions)

        # Write rejected transactions
        with open(rejected_file, mode='w', newline='', encoding='utf-8') as outfile:
            rejected_headers = headers + ['error']
            writer = csv.DictWriter(outfile, fieldnames=rejected_headers)
            writer.writeheader()
            writer.writerows(rejected_transactions)

        # Print summary
        print("--- Transaction Processing Summary ---")
        print(f"Total rows processed: {total_rows}")
        print(f"Rows accepted: {len(valid_transactions)}")
        print(f"Rows rejected: {len(rejected_transactions)}")
        print("\nRejection Reasons:")
        if not rejection_counts:
            print("- None")
        else:
            sorted_reasons = sorted(rejection_counts.items())
            for reason, count in sorted_reasons:
                print(f"- {reason}: {count}")

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    INPUT_CSV = 'transactions.csv'
    OUTPUT_CSV = 'output.csv'
    REJECTED_CSV = 'rejected.csv'
    process_transactions(INPUT_CSV, OUTPUT_CSV, REJECTED_CSV)
