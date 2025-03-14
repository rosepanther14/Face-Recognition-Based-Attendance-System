# Biometric Face Recognition Attendance System

## 📌 Project Overview
This is a **Face Recognition-based Attendance System** using Python, OpenCV, and SQLite. It utilizes facial recognition to mark attendance, export logs to Excel, and store records in Google Sheets.

## 🔧 Features
- **Face Registration**: Users can register their faces in the database.
- **Real-time Face Recognition**: Detects faces and marks attendance.
- **Attendance Records**:
  - View attendance logs.
  - Export attendance to Excel.
  - Store data in Google Sheets for remote access.
- **Graphical User Interface (GUI)**: Built using Tkinter.
- **Dark Mode & Light Mode Switch**: Improves UI experience.
- **Bug Fixes & Optimizations**:
  - Adjustable recognition tolerance.
  - Proper database handling.
  - Smooth UI interactions.

## 🛠️ Installation Steps
1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/Biometric-Face-Recognition-Attendance.git
   cd Biometric-Face-Recognition-Attendance
   ```
2. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
3. **Set Up Database**
   ```sh
   python database_setup.py
   ```
4. **Register Users**
   ```sh
   python register_user.py
   ```
5. **Run Attendance System**
   ```sh
   python gui_attendance.py
   ```

## 🚀 How to Use
- **Start the GUI**: Run `gui_attendance.py`
- **Register Faces**: Enter your name and press 'S' to capture your face.
- **Recognize Faces**: The system will mark attendance upon successful detection.
- **View & Export Attendance**:
  - Click "View Attendance" to see logs.
  - Click "Export to Excel" or "Export to Google Sheets".
- **Clear Records**: Click "Clear Attendance" to reset logs.

## 🎨 GUI & Cloud Integration Details
- **Tkinter-based UI**
- **Real-time face recognition with OpenCV**
- **Stores data locally (SQLite) and remotely (Google Sheets)**

## 🐞 Common Bugs & Fixes
| Bug | Solution |
|------|----------|
| Python 3.10+ issues | Downgrade to Python 3.9 |
| NumPy version 2 errors | Install NumPy 1.x |
| Dlib installation error | Manually download `dlib.whl` |
| Face recognition mismatch | Adjust tolerance to 0.4 |

## 🎯 Future Enhancements
- Web-based version
- Mobile app integration
- Multi-user authentication
- AI-based attendance insights
---
### **Developed by Mohammed Fahad Nawaz Khan** 

