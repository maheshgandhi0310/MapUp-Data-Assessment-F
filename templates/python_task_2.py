import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    distance_matrix = df.pivot(index='id_start', columns='id_end', values='distance')
    distance_matrix = distance_matrix.fillna(0)
    distance_matrix = distance_matrix.add(distance_matrix.T, fill_value=0)
    
    for col in distance_matrix.columns:
        for row in distance_matrix.index:
            if row != col:
                for via in distance_matrix.index:
                    if via != col and via != row:
                        if distance_matrix.at[row, via] != 0 and distance_matrix.at[via, col] != 0:
                            if distance_matrix.at[row, col] == 0 or distance_matrix.at[row, col] > distance_matrix.at[row, via] + distance_matrix.at[via, col]:
                                distance_matrix.at[row, col] = distance_matrix.at[row, via] + distance_matrix.at[via, col]
    
    return distance_matrix


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    unrolled_matrix = matrix.stack().reset_index()
    unrolled_matrix.columns = ['id_start', 'id_end', 'distance']
    unrolled_matrix = unrolled_matrix[unrolled_matrix['id_start'] != unrolled_matrix['id_end']]
    
    return unrolled_matrix


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    avg_distance = df[df['id_start'] == reference_value]['distance'].mean()
    lower_bound = avg_distance * 0.9
    upper_bound = avg_distance * 1.1
    within_threshold = df[(df['id_start'] != reference_value) & (df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]['id_start'].unique()
    within_threshold = sorted(within_threshold)
    
    return within_threshold


def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    rate_coefficients = {'moto': 0.8, 'car': 1.2, 'rv': 1.5, 'bus': 2.2, 'truck': 3.6}
    
    for vehicle in rate_coefficients:
        df[vehicle] = df['distance'] * rate_coefficients[vehicle]
    
    return df


def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    days_mapping = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
    
    df['start_day'] = df['start_timestamp'].dt.dayofweek.map(days_mapping)
    df['end_day'] = df['end_timestamp'].dt.dayofweek.map(days_mapping)
    
    weekday_discounts = {
        (time(0, 0, 0), time(10, 0, 0)): 0.8,
        (time(10, 0, 0), time(18, 0, 0)): 1.2,
        (time(18, 0, 0), time(23, 59, 59)): 0.8
    }
    weekend_discount = 0.7
    
    def calculate_rate(row):
        if row['start_day'] in ['Saturday', 'Sunday']:
            return weekend_discount
        else:
            for time_range, discount_factor in weekday_discounts.items():
                start_time, end_time = time_range
                if start_time <= row['start_timestamp'].time() <= end_time:
                    return discount_factor
            return 1.0
    
    for vehicle in ['moto', 'car', 'rv', 'bus', 'truck']:
        df[vehicle] = df.apply(lambda row: row[vehicle] * calculate_rate(row), axis=1)
    
    df['start_time'] = df['start_timestamp'].dt.time
    df['end_time'] = df['end_timestamp'].dt.time
    df.drop(['start_timestamp', 'end_timestamp'], axis=1, inplace=True)

    return df


data_task2 = pd.read_csv('dataset-3.csv')

result_distance_matrix = calculate_distance_matrix(data_task2)
result_unrolled_matrix = unroll_distance_matrix(result_distance_matrix)
reference_id = 1  # Set your reference ID here
result_within_threshold = find_ids_within_ten_percentage_threshold(result_unrolled_matrix, reference_id)
result_toll_rates = calculate_toll_rate(result_unrolled_matrix)
result_time_based_toll_rates = calculate_time_based_toll_rates(result_within_threshold)

print("Result Distance Matrix:")
print(result_distance_matrix)

print("\nResult Unrolled Distance Matrix:")
print(result_unrolled_matrix)

print("\nResult IDs within Ten Percentage Threshold:")
print(result_within_threshold)

print("\nResult Toll Rates:")
print(result_toll_rates)

print("\nResult Time-Based Toll Rates:")
print(result_time_based_toll_rates)