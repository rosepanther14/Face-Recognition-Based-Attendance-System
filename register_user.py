import cv2
import face_recognition
import sqlite3
import numpy as np

# Connect to database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

def register_user(name):
    cam = cv2.VideoCapture(0)  # Open laptop camera
    print("Press 's' to capture your face.")

    while True:
        ret, frame = cam.read()
        cv2.imshow("Capture Face", frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):  # Press 's' to save face
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  
            face_encodings = face_recognition.face_encodings(rgb_frame)

            if face_encodings:
                encoded_face = face_encodings[0].tobytes() 
                c.execute("INSERT INTO users (name, encoding) VALUES (?, ?)", (name, encoded_face))
                conn.commit()
                print("Face Registered Successfully!")
                break
            else:
                print("No face detected! Try again.")

    cam.release()
    cv2.destroyAllWindows()

name = input("Enter your name: ")
register_user(name)
