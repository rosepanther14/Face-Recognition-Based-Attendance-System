import sqlite3

# Create a database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

 
c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                encoding BLOB)''')


c.execute('''CREATE TABLE IF NOT EXISTS attendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                timestamp TEXT)''')

conn.commit()
conn.close()

print("Database and tables created successfully!")
