import sqlite3

# Connect to the database (creates the database file if it doesn't exist)
conn = sqlite3.connect('TaxiBooking.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create a table named 'driver'
cursor.execute('''
    CREATE TABLE IF NOT EXISTS driver (
        driverid INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        number TEXT,
        address TEXT,
        email TEXT,
        password TEXT)''')
driver_data=[
    ('Peter', 9865220110, 'Bhaktapur', 'peter@gmail.com', 'peter'),
    ('Chris', 9800359750, 'New Road', 'chris@gmail.com', 'chris'),
    ('Joe', 9899658500, 'Kalanki', 'joe@gmail.com', 'joe'),
    ('Monica', 9833100596, 'Pulchowk', 'monica@gmail.com', 'monica')
]

cursor.executemany('INSERT INTO driver (name, number, address, email, password) VALUES (?, ?, ?, ?, ?)', driver_data)

# Commit the changes and close the connection
conn.commit()
conn.close()

