import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    matrix = df.pivot(index='id_1', columns='id_2', values='car')
    matrix = matrix.fillna(0)
    for col in matrix.columns:
        matrix.loc[col, col] = 0
    return matrix


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')], labels=['low', 'medium', 'high'])
    type_counts = df['car_type'].value_counts().to_dict()
    sorted_type_counts = dict(sorted(type_counts.items()))
    return sorted_type_counts


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    mean_bus = df['bus'].mean()
    bus_indexes = df[df['bus'] > 2 * mean_bus].index.tolist()
    bus_indexes.sort()
    return bus_indexes


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    avg_truck = df.groupby('route')['truck'].mean()
    filtered_routes = avg_truck[avg_truck > 7].index.tolist()
    filtered_routes.sort()
    return filtered_routes


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    modified_matrix = matrix.copy()
    modified_matrix = modified_matrix.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    modified_matrix = modified_matrix.round(1)
    return modified_matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'])
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'])
    incorrect_timestamps = (df['end_timestamp'] - df['start_timestamp'] != pd.Timedelta(days=1)) | (df['end_timestamp'].dt.dayofweek - df['start_timestamp'].dt.dayofweek != 6)
    incorrect_timestamps = incorrect_timestamps.groupby([df['id'], df['id_2']]).any()
    return incorrect_timestamps

data_task1 = pd.read_csv('dataset-1.csv')
data_task2 = pd.read_csv('dataset-2.csv')

result_car_matrix = generate_car_matrix(data_task1)
result_type_count = get_type_count(data_task1)
result_bus_indexes = get_bus_indexes(data_task1)
result_filtered_routes = filter_routes(data_task1)
result_modified_matrix = multiply_matrix(result_car_matrix)
result_time_check = time_check(data_task2)

print("Result Car Matrix:")
print(result_car_matrix)

print("\nResult Car Type Count:")
print(result_type_count)

print("\nResult Bus Count Indexes:")
print(result_bus_indexes)

print("\nResult Filtered Routes:")
print(result_filtered_routes)

print("\nResult Modified Matrix:")
print(result_modified_matrix)

print("\nResult Time Check:")
print(result_time_check)
