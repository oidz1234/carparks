import sqlite3

# Connect to the SQLite database (this will create a new database file if it doesn't exist)
conn = sqlite3.connect('parking_data.db')

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Create a table to store parking data without enforcing uniqueness on the timestamp
cursor.execute('''
    CREATE TABLE IF NOT EXISTS parking_history (
        timestamp INTEGER,
        name TEXT,
        code TEXT,
        spaces INTEGER,
        type TEXT,
        status TEXT,
        carparkOpen BOOLEAN,
        carparkInformation TEXT,
        numberOfUnusableSpaces INTEGER,
        numberOfSpacesConsideredLow INTEGER
    )
''')

# Commit changes and close the connection
conn.commit()
conn.close()
