import sqlite3
import sys
from datetime import datetime, timedelta, timezone

def get_data_for_carpark(carpark_name, time_period='daily'):
    conn = sqlite3.connect('parking_data.db')
    cursor = conn.cursor()

    # Calculate the start date based on the selected time period
    if time_period == 'daily':
        start_date = datetime.now() - timedelta(days=1)
    elif time_period == 'weekly':
        start_date = datetime.now() - timedelta(weeks=1)
    elif time_period == 'monthly':
        start_date = datetime.now() - timedelta(weeks=4)
    else:
        # Default to daily if an invalid time period is provided
        start_date = datetime.now() - timedelta(days=1)

    # Convert start_date to timestamp
    start_timestamp = int(start_date.timestamp())

    # Retrieve data for a specific car park and time period from the table
    cursor.execute('''
        SELECT timestamp, spaces
        FROM parking_history
        WHERE name = ? AND timestamp >= ?
    ''', (carpark_name, start_timestamp))
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Convert timestamp and spaces data to list of tuples
    data = [(datetime.utcfromtimestamp(row[0]).replace(tzinfo=timezone.utc), int(row[1])) for row in rows]

    return data

def calculate_zero_space_percentage(carpark_data):
    total_time = carpark_data[-1][0] - carpark_data[0][0]  # Total time period
    zero_space_time = sum(1 for _, spaces in carpark_data if spaces == 0)  # Time with 0 spaces

    zero_space_percentage = (zero_space_time / total_time.total_seconds()) * 100

    return zero_space_percentage

def print_zero_space_percentages(carpark_names, time_period='daily'):
    for carpark_name in carpark_names:
        carpark_data = get_data_for_carpark(carpark_name, time_period)
        zero_space_percentage = calculate_zero_space_percentage(carpark_data)

        print(f"The percentage of time with 0 spaces in {carpark_name} over the last {time_period} is: {zero_space_percentage:.2f}%")

if __name__ == "__main__":
    all_carpark_names = ['Green Street', 'Minden Place', 'Patriotic Street', 'Sand Street', 'Pier Road', 'Les Jardin']
    time_period = 'daily'  # Replace with the desired time period
    #time_period = sys.argv[1]


    print_zero_space_percentages(all_carpark_names, time_period)

