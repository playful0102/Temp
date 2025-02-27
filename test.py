def get_moving_averages(monthly_averages_list):
    """
    Calculates the 4-month weighted moving average (WMA) for all months in the dataset.
    The weights are [4, 3, 2, 1], with the most recent month given the highest weight.
    
    :param monthly_averages_list: List of tuples, each containing (month, average_price).
    :return: A list of tuples containing (month, WMA) for all valid months.
    """
    # Reverse the list to make sure it's in chronological order (ascending order)
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

    return moving_averages_list


monthly_averages_list = [
    ('1/2021', 4000),
    ('2/2021', 4050),
    ('3/2021', 4100),
    ('4/2021', 4150),
    ('5/2021', 4200),
    ('6/2021', 4250),
    # More months...
]
moving_averages = get_moving_averages(monthly_averages_list)
print(moving_averages)
