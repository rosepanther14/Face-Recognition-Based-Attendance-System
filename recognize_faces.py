import cv2
import face_recognition
import sqlite3
import numpy as np
from datetime import datetime

# Connect to database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Load registered users
c.execute("SELECT name, encoding FROM users")
registered_users = c.fetchall()

known_face_encodings = []
known_face_names = []

for name, enc in registered_users:
    known_face_encodings.append(np.frombuffer(enc, dtype=np.float64))
    known_face_names.append(name)

# Open camera
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect faces
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for encoding, loc in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, encoding, tolerance=0.4)
        face_distances = face_recognition.face_distance(known_face_encodings, encoding)
        name = "Unknown"

        if True in matches:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                # Mark attendance
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO attendance (name, timestamp) VALUES (?, ?)", (name, timestamp))
                conn.commit()

        # Draw a box around the face
        top, right, bottom, left = loc
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imshow("Face Recognition", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit
        break

cam.release()
cv2.destroyAllWindows()
