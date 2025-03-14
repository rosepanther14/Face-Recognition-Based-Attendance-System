import sqlite3
import numpy as np

# Connect to the database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Fetch all users
c.execute("SELECT name, encoding FROM users")
users = c.fetchall()

# Display stored users
for user in users:
    name = user[0]
    encoding = np.frombuffer(user[1], dtype=np.float64)  # Convert bytes to array
    print(f"Name: {name}, Encoding: {encoding[:5]}...")  # Show first 5 values

conn.close()
print("Users retrieved successfully")