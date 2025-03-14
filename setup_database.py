import sqlite3

# Create (or connect to) a database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Create table for storing users (name and their face encoding)
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                encoding BLOB)''')

# Create table for storing attendance logs
c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                timestamp TEXT)''')

# Save changes and close the connection
conn.commit()
conn.close()

print("Database and tables created successfully!")
