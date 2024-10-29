import csv
import numpy as np
import pandas as pd
from datetime import datetime

def read_csv_first_row(file_path):
    """Read the first row of a CSV file, handle extra commas, whitespace, and replace empty fields with 0."""
    with open(file_path, newline='') as csvfile:
        # Read the first line and handle extra commas and whitespace
        line = csvfile.readline().strip()
        # Split by comma, strip whitespace from each item, and replace empty strings with 0
        first_row = [float(value.strip()) if value.strip() else 0.0 for value in line.split(',')]
    return np.array(first_row, dtype=float)

def extend_data_with_zeros(data, interval1):
    """Extend data by appending interval1 zeros."""
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
        # If specified_length is None, use the full length of the columns
        specified_length = extended_rows.shape[1]
    elif specified_length > extended_rows.shape[1]:
        # If specified_length exceeds the number of columns, adjust to the number of columns
        specified_length = extended_rows.shape[1]
    
    # Slice the extended_rows to only include up to the specified_length
    sliced_rows = extended_rows[:, :specified_length]
    
    # Calculate the sum of each column in the sliced rows
    return np.sum(sliced_rows, axis=0)

# 현재 날짜와 시간을 기반으로 파일명을 생성하는 함수
def get_unique_filename(base_name, extension):
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d_%H%M%S")  # 예: 20240719_103000
    return f"{base_name}_{timestamp}.{extension}"

def main(csv_file_path, output_file):
    # Define intervals
    interval1_range = range(2, 60, 2)  # interval1 from 2 to 60, step 2
    interval2_range = range(2, 60, 2)  # interval2 from 2 to 60, step 2
    rows = 16                      # Number of rows to generate
    min_length = 1440             # Minimum length of the data

    # Read the first row from CSV
    first_row = read_csv_first_row(csv_file_path)

    # Prepare lists to hold results
    results = []

    # Iterate over all combinations of interval1 and interval2
    for interval1 in interval1_range:
        for interval2 in interval2_range:
            # Process data
            long_data = generate_long_data(first_row, interval1, min_length)
            extended_rows = add_rows(long_data, rows, interval2)
            #전체 길이에 대한 합산을 계산, 트레이 투입이 중단되는 경우의 피크를 검출
            column_sums = calculate_column_sums(extended_rows)
            
            #지정된 길이까지 합산 값을 계산, 트레이 투입이 연속적인 경우의 피크를 검출
            #column_sums = calculate_column_sums(extended_rows, min_length)
            max_sum = np.max(column_sums)
            min_sum = np.min(column_sums)
            
            # Store results
            results.append({
                'Interval1': interval1,
                'Interval2': interval2,
                'Max Sum': max_sum,
                'Min Sum': min_sum
            })

    # Convert results to DataFrame and save to Excel
    df_results = pd.DataFrame(results)

    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_results.to_excel(writer, sheet_name='Results', index=False)

# Example usage
if __name__ == "__main__":
    # Define the input CSV file path and output file name
    csv_file_path = 'data.csv'
    output_file = get_unique_filename("results", "xlsx")

    main(csv_file_path, output_file)