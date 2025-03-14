import sqlite3

# Connect to database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Retrieve attendance records
c.execute("SELECT * FROM attendance")
records = c.fetchall()

print("\nAttendance Records:")
for row in records:
    print(f"ID: {row[0]}, Name: {row[1]}, Timestamp: {row[2]}")

conn.close()
print("\nAttendance records retrieved successfully!")