import requests
import time
import sqlite3
from datetime import datetime




unix_time = int(time.time())
url = f'https://www.gov.je/_layouts/15/C5.Gov.Je.CarParks/proxy.aspx?_={unix_time}'



def insert_parking_data(data):
    conn = sqlite3.connect('parking_data.db')
    cursor = conn.cursor()

    # Get the current timestamp
    timestamp = int(datetime.timestamp(datetime.now()))

    # Insert the data into the table
    cursor.execute('''
        INSERT INTO parking_history (
            timestamp, name, code, spaces, type, status, carparkOpen,
            carparkInformation, numberOfUnusableSpaces, numberOfSpacesConsideredLow
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        timestamp,
        data['name'],
        data['code'],
        data['spaces'],
        data['type'],
        data['status'],
        data['carparkOpen'],
        data['carparkInformation'],
        data['numberOfUnusableSpaces'],
        data['numberOfSpacesConsideredLow']
    ))

    # Commit changes and close the connection
    conn.commit()
    conn.close()


response = requests.get(url)

if response.status_code == 200:
    data = response.json()
else:
    print(f"Error: {response.status_code}")



carparks_list = data['carparkData']['Jersey']['carpark']
for entry in carparks_list:
    insert_parking_data(entry)

def print_latest_values():
    conn = sqlite3.connect('parking_data.db')
    cursor = conn.cursor()

    # SQL query to retrieve the latest values for each car park
    cursor.execute('''
        SELECT code, name, spaces, type, status
        FROM parking_history
        WHERE (timestamp, code) IN (
            SELECT MAX(timestamp), code
            FROM parking_history
            GROUP BY code
        )
    ''')

    # Fetch all the rows
    rows = cursor.fetchall()

    # Close the connection
    conn.close()

    # Print the latest values for each car park
    print("Latest values for each car park:")
    for row in rows:
        code, name, spaces, car_type, status = row
        print(f"Carpark {code}: {name}, Spaces: {spaces}, Type: {car_type}, Status: {status}")

# Call the function to print the latest values
#print_latest_values()


