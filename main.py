import csv

def get_records_list(csv_file_name):
    """
    Reads the CSV file and processes the data.
    Ensures the date column remains in MM/DD/YYYY format.
    :param csv_file_name: Name of the CSV file to read.
    :return: A list of lists (records_list).
    """
    records_list = []
    try:
        with open(csv_file_name, 'r') as file:
            csv_reader = csv.reader(file)
            header = next(csv_reader)  # Skip the header if present
            for row in csv_reader:
                if len(row) > 0:
                    # Validate the date format (MM/DD/YYYY)
                    #date_parts = row[0].split("/")
                    # The date is already in MM/DD/YYYY format, no changes needed
                    records_list.append(row)
    except FileNotFoundError:
        print(f"Error: The file {csv_file_name} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")
    return records_list


def get_monthly_averages(records_list):
    """
    Calculates average monthly prices.
    :param records_list: A list of lists containing stock data.
    :return: A list of tuples with the month and the average price.
    """
    from collections import defaultdict
    
    monthly_totals = defaultdict(lambda: {'total_sales': 0, 'total_volume': 0})
    for record in records_list:
        try:
            date_parts = record[0].split('/')  # Date is MM/DD/YYYY
            month_year = f"{date_parts[0]}/{date_parts[2]}"  # MM/YYYY
            volume = int(record[6])  # Volume
            adj_close = float(record[5])  # Adj Close
            
            # Update totals
            monthly_totals[month_year]['total_sales'] += volume * adj_close
            monthly_totals[month_year]['total_volume'] += volume
        except (ValueError, IndexError):
            print(f"Skipping invalid record: {record}")
    
    # Calculate averages
    monthly_averages_list = []
    for month_year, totals in monthly_totals.items():
        if totals['total_volume'] > 0:
            avg_price = totals['total_sales'] / totals['total_volume']
            monthly_averages_list.append((month_year, avg_price))
    return monthly_averages_list

def get_moving_averages(monthly_averages_list):
    """
    Calculates the 4-month weighted moving average (WMA) for all months in the dataset.
    The weights are [4, 3, 2, 1], with the most recent month given the highest weight.
    
    :param monthly_averages_list: List of tuples, each containing (month, average_price).
    :return: A list of tuples containing (month, WMA) for all valid months.
    """
    # Ensure the list is sorted chronologically (ascending order)
    monthly_averages_list.reverse()

    # Initialize the list to store moving averages
    moving_averages_list = []

    # Weights for the 4-month WMA: most recent month has the highest weight
    weights = [4, 3, 2, 1]
    total_weight = sum(weights)  # The total weight sum will be 10

    # Loop through the list, starting from the 4th month
    for i in range(3, len(monthly_averages_list)):
        # Get the previous 4 months and their corresponding average prices
        subset = monthly_averages_list[i-3:i+1]

        # Calculate the weighted sum of the 4 months
        weighted_sum = sum(subset[j][1] * weights[j] for j in range(4))

        # Calculate the WMA by dividing the weighted sum by the total weight
        wma = weighted_sum / total_weight

        # Append the current month and its WMA to the result list
        moving_averages_list.append((subset[3][0], wma))  # Take the month from the last month in the subset
    print(moving_averages_list)
    return moving_averages_list


def find_best_and_worst_months(moving_averages_list):
    """
    Finds the best and worst months based on WMA prices.
    :param moving_averages_list: List of tuples with month and WMA prices.
    :return: Two tuples (best_month, worst_month).
    """
    if not moving_averages_list:
        return None, None

    best_month = max(moving_averages_list, key=lambda x: x[1])
    worst_month = min(moving_averages_list, key=lambda x: x[1])
    print(moving_averages_list)
    return best_month, worst_month

def main():
    csv_file_name = input("Enter the CSV file name: ")
    output_file_name = "sp500_output.txt"
    
    # Step 1: Get records list
    records_list = get_records_list(csv_file_name)
    if not records_list:
        print("No valid records found.")
        return
    
    # Step 2: Calculate monthly averages
    monthly_averages_list = get_monthly_averages(records_list)
    
    # Step 3: Calculate moving averages
    moving_averages_list = get_moving_averages(monthly_averages_list)
    
    # Step 4: Find best and worst months
    best_month, worst_month = find_best_and_worst_months(moving_averages_list)
    
    # Step 5: Write output to file
    try:
        with open(output_file_name, 'w') as output_file:
            output_file.write("The best month for S&P 500:\n")
            # Convert date to MM-YYYY with "-" instead of "/"
            output_file.write(f"{best_month[0].replace('/', '-')}, {best_month[1]:.2f}\n")
            output_file.write("The worst month for S&P 500:\n")
            output_file.write(f"{worst_month[0].replace('/', '-')}, {worst_month[1]:.2f}\n")
        print(f"The enetered CSV file name: {csv_file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")

main()