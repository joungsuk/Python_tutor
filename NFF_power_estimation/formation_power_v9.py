import numpy as np
import pandas as pd
from datetime import datetime

def read_csv_first_row(file_path):
    """Read the first row of a CSV file, handle extra commas, whitespace, and replace empty fields with 0."""
    with open(file_path, newline='') as csvfile:
        line = csvfile.readline().strip()
        # Split by comma, strip whitespace from each item, and replace empty strings with 0
        first_row = [float(value.strip()) if value.strip() else 0.0 for value in line.split(',')]
    return np.array(first_row, dtype=float)

def extend_data_with_zeros(data, interval1):
    """Extend data by appending `interval1` zeros."""
    return np.concatenate((data, np.zeros(interval1, dtype=float)))

def generate_long_data(data, interval1, min_length=1440):
    """Generate a long data sequence by repeating the extended data."""
    extended_data = extend_data_with_zeros(data, interval1)
    repeated_data = np.tile(extended_data, (min_length // len(extended_data)) + 1)
    return repeated_data[:min_length]

def add_rows(base_data, rows, interval2):
    """Add rows to the base data with (row - 1) * interval2 leading zeros and pad with trailing zeros to match the length."""
    max_length = len(base_data) + (rows - 1) * interval2
    extended_rows = np.zeros((rows, max_length), dtype=float)
    for i in range(rows):
        start_idx = i * interval2
        extended_rows[i, start_idx:start_idx + len(base_data)] = base_data
    return extended_rows

def calculate_column_sums(extended_rows, specified_length=None):
    """Calculate the sum of each column in the extended rows up to a specified length.
       If specified_length is None, sum all columns."""
    if specified_length is None:
        specified_length = extended_rows.shape[1]
    elif specified_length > extended_rows.shape[1]:
        specified_length = extended_rows.shape[1]
    
    sliced_rows = extended_rows[:, :specified_length]
    return np.sum(sliced_rows, axis=0)

def get_unique_filename(base_name, interval1, interval2, extension):
    """Generate a unique filename with current date, time, and specified intervals."""
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # Example: 20240719_103000
    return f"{base_name}_interval1-{interval1}_interval2-{interval2}_{timestamp}.{extension}"

def save_results_to_excel(extended_rows, column_sums, max_sum, min_sum, output_file):
    """Save results to an Excel file with unique filename."""
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # Save extended_rows as DataFrame
        df_extended_rows = pd.DataFrame(extended_rows)
        df_extended_rows.to_excel(writer, sheet_name='Extended Rows', index=False)
        
        # Save column_sums as DataFrame (transposed to match the format)
        df_column_sums = pd.DataFrame(column_sums, columns=['Column Sum']).T
        df_column_sums.to_excel(writer, sheet_name='Column Sums', index=False)
        
        # Save max_sum and min_sum as DataFrame
        df_summary = pd.DataFrame({
            'Max Sum': [max_sum],
            'Min Sum': [min_sum]
        })
        df_summary.to_excel(writer, sheet_name='Summary', index=False)

    print(f"Results have been saved to {output_file}")

def main(csv_file_path, interval1, interval2, rows, output_file):
    min_length = 1440             # Minimum length of the data
    # Step 1: Read the first row from CSV
    first_row = read_csv_first_row(csv_file_path)
    print(f"Original data: {first_row}")

    # Step 2 & 3: Extend data with zeros and generate long data
    long_data = generate_long_data(first_row, interval1)
    print(f"Extended long data (length {len(long_data)}): {long_data}")

    # Step 4: Add rows with (row - 1) * interval2 leading zeros and pad with trailing zeros
    extended_rows = add_rows(long_data, rows, interval2)
    for i, row in enumerate(extended_rows):
        print(f"Row {i + 1} (length {len(row)}): {row}")

    # Step 5: Calculate column sums
    column_sums = calculate_column_sums(extended_rows, min_length)
    #column_sums = calculate_column_sums(extended_rows)
    print(f"Column sums: {column_sums}")

    # Find and print the maximum and minimum column sums
    max_sum = np.max(column_sums)
    min_sum = np.min(column_sums)
    print(f"Maximum column sum: {max_sum}")
    print(f"Minimum column sum: {min_sum}")

    # Save results to Excel
    save_results_to_excel(extended_rows, column_sums, max_sum, min_sum, output_file)

# Example usage
if __name__ == "__main__":
    # Define the input CSV file path and intervals
    csv_file_path = 'data.csv'
    interval1 = 2  # Number of zeros to append after the first row data
    interval2 = 10   # Number of leading zeros to add to each new row
    rows = 100        # Number of rows to generate
    output_file = get_unique_filename("results", interval1, interval2, "xlsx")

    main(csv_file_path, interval1, interval2, rows, output_file)