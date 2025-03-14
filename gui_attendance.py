import cv2
import face_recognition
import sqlite3
import numpy as np
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import pandas as pd
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Connect to SQLite Database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("credentials.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet 
sheet = client.open("attendance-list").sheet1

# Custom message box
def custom_messagebox(title, message):
    msg_box = tk.Toplevel()
    msg_box.title(title)
    msg_box.geometry("300x150")
    msg_box.configure(bg="#333333")

    label = ttk.Label(msg_box, text=message, font=("Montserrat", 14), background="#333333", foreground="#ffffff")
    label.pack(pady=20)

    ok_button = ttk.Button(msg_box, text="OK", command=msg_box.destroy)
    ok_button.pack(pady=10)

    msg_box.transient(root)
    msg_box.grab_set()
    root.wait_window(msg_box)

# GUI Application
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Face Recognition Attendance")
        self.root.geometry("1920x1080")

        # Set a stylish font
        self.font = ("Montserrat", 16)

        # Create a frame for the content
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(fill=tk.BOTH, expand=True)

        # Define styles for light and dark themes
        self.style = ttk.Style()
        self.light_theme()

        ttk.Label(self.content_frame, text="Face Recognition Attendance", font=("Montserrat", 30)).pack(pady=20)
        
        self.start_btn = ttk.Button(self.content_frame, text="Start Attendance", command=self.start_attendance)
        self.start_btn.pack(pady=10)

        self.export_btn = ttk.Button(self.content_frame, text="Export to Excel", command=self.export_to_excel)
        self.export_btn.pack(pady=10)

        self.export_google_btn = ttk.Button(self.content_frame, text="Export to Google Sheets", command=self.export_to_google_sheets)
        self.export_google_btn.pack(pady=10)

        self.clear_btn = ttk.Button(self.content_frame, text="Clear Attendance", command=self.clear_attendance)
        self.clear_btn.pack(pady=10)

        # Add a button to view attendance in fullscreen mode
        self.view_btn = ttk.Button(self.content_frame, text="View Attendance", command=self.view_attendance)
        self.view_btn.pack(pady=10)

        # Add a button to toggle between light and dark themes
        self.theme_btn = ttk.Button(self.content_frame, text="Switch to Dark Theme", command=self.toggle_theme)
        self.theme_btn.pack(pady=10)

        self.quit_btn = ttk.Button(self.content_frame, text="Quit", command=root.quit)
        self.quit_btn.pack(pady=10)

    def light_theme(self):
        # Configure light theme
        self.style.theme_use('default')
        self.style.configure("TButton", font=self.font, padding=10, background="#f0f0f0", foreground="#000000",
                             activebackground="#d9d9d9", activeforeground="#000000", borderwidth=1, relief="flat")
        self.style.map("TButton", background=[("active", "#d9d9d9")], foreground=[("active", "#000000")])
        self.style.configure("TLabel", font=("Montserrat", 30), background="#f0f0f0", foreground="#000000")
        self.root.configure(bg="#f0f0f0")
        self.content_frame.configure(bg="#f0f0f0")

    def dark_theme(self):
        # Configure dark theme
        self.style.theme_use('clam')
        self.style.configure("TButton", font=self.font, padding=10, background="#333333", foreground="#ffffff",
                             activebackground="#555555", activeforeground="#ffffff", borderwidth=1, relief="flat")
        self.style.map("TButton", background=[("active", "#555555")], foreground=[("active", "#ffffff")])
        self.style.configure("TLabel", font=("Montserrat", 30), background="#333333", foreground="#ffffff")
        self.root.configure(bg="#333333")
        self.content_frame.configure(bg="#333333")

    def toggle_theme(self):
        # Toggle between light and dark themes
        if self.theme_btn.cget("text") == "Switch to Dark Theme":
            self.dark_theme()
            self.theme_btn.config(text="Switch to Light Theme")
        else:
            self.light_theme()
            self.theme_btn.config(text="Switch to Dark Theme")

    def start_attendance(self):
        custom_messagebox("Info", "Starting Face Recognition")

        # Load known face encodings
        c.execute("SELECT name, encoding FROM users")
        users = c.fetchall()
        known_names = []
        known_encodings = []

        for user in users:
            name = user[0]
            encoding = np.frombuffer(user[1], dtype=np.float64)
            known_names.append(name)
            known_encodings.append(encoding)

        # Open webcam
        cam = cv2.VideoCapture(0)
        while True:
            ret, frame = cam.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=0.5)
                face_distances = face_recognition.face_distance(known_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    name = known_names[best_match_index]
                    print(f"Detected: {name}")

                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute("INSERT INTO attendance (name, timestamp) VALUES (?, ?)", (name, timestamp))
                    conn.commit()

                    # Smooth transition for marking attendance
                    self.root.after(500, lambda: custom_messagebox("Attendance", f"Attendance marked for {name}"))
                    cam.release()
                    cv2.destroyAllWindows()
                    return  # Exit the function to close the application

                else:
                    print("Unknown Face Detected")
                    self.root.after(500, lambda: custom_messagebox("Warning", "Unknown Face Detected!"))

            cv2.imshow("Face Recognition", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cam.release()
        cv2.destroyAllWindows()

    def export_to_excel(self):
        try:
            c.execute("SELECT * FROM attendance")
            records = c.fetchall()
            df = pd.DataFrame(records, columns=["ID", "Name", "Timestamp"])
            df.to_excel("attendance_records.xlsx", index=False)
            self.root.after(500, lambda: custom_messagebox("Export", "Attendance records exported to attendance_records.xlsx"))
        except PermissionError:
            self.root.after(500, lambda: custom_messagebox("Error", "CLOSE THE EXCEL FIRST!"))
        except Exception as e:
            self.root.after(500, lambda: custom_messagebox("Error", f"An error occurred: {e}"))

    def export_to_google_sheets(self):
        try:
            c.execute("SELECT * FROM attendance")
            records = c.fetchall()
            df = pd.DataFrame(records, columns=["ID", "Name", "Timestamp"])
            sheet.clear()
            sheet.update([df.columns.values.tolist()] + df.values.tolist())
            self.root.after(500, lambda: custom_messagebox("Export", "Attendance records exported to Google Sheets"))
        except Exception as e:
            self.root.after(500, lambda: custom_messagebox("Error", f"An error occurred: {e}"))

    def clear_attendance(self):
        try:
            # Clear the SQLite database
            c.execute("DELETE FROM attendance")
            c.execute("DELETE FROM sqlite_sequence WHERE name='attendance'")
            conn.commit()

            # Clear the Google Sheet
            sheet.clear()

            self.root.after(500, lambda: custom_messagebox("Clear", "Attendance records cleared"))
        except Exception as e:
            self.root.after(500, lambda: custom_messagebox("Error", f"An error occurred: {e}"))

    # Add a method to view attendance in fullscreen mode
    def view_attendance(self):
        try:
            # Create a new fullscreen window
            view_window = tk.Toplevel(self.root)
            view_window.attributes('-fullscreen', True)
            view_window.title("Attendance Records")

            # Create a Treeview widget to display the attendance records
            tree = ttk.Treeview(view_window, columns=("ID", "Name", "Timestamp"), show='headings')
            tree.heading("ID", text="ID")
            tree.heading("Name", text="Name")
            tree.heading("Timestamp", text="Timestamp")
            tree.pack(expand=True, fill=tk.BOTH)

            # Fetch attendance records from the database
            c.execute("SELECT * FROM attendance")
            records = c.fetchall()

            # Insert records into the Treeview
            for record in records:
                tree.insert("", tk.END, values=record)

            # Add a button to close the fullscreen window
            close_btn = ttk.Button(view_window, text="Close", command=view_window.destroy)
            close_btn.pack(pady=20)
        except Exception as e:
            self.root.after(500, lambda: custom_messagebox("Error", f"An error occurred: {e}"))

# Run the Application
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()