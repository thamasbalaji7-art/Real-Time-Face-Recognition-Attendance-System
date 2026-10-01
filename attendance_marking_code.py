import cv2
import face_recognition
import numpy as np
import os
from datetime import datetime, timedelta
from openpyxl import Workbook, load_workbook

# Folder with saved reference images
path = "reference_images"

# Create attendance file name based on 10-minute interval
now = datetime.now()
slot_start = now - timedelta(minutes=now.minute % 2, seconds=now.second, microseconds=now.microsecond)
slot_str = slot_start.strftime("%H")
attendance_file = f"Attendance-{slot_str} O'Clock.xlsx"

# Load all reference images and names
images = []
names = []

for file in os.listdir(path):
    if file.endswith(".jpg"):
        img = cv2.imread(os.path.join(path, file))
        images.append(img)
        name = os.path.splitext(file)[0].split("_")[1]  # filename like face_Name.jpg
        names.append(name)

# Encode reference faces
print("Encoding known faces...")
known_encodings = []
for img in images:
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    encode = face_recognition.face_encodings(rgb_img)
    if encode:
        known_encodings.append(encode[0])

print(f"✅ Loaded {len(known_encodings)} known faces.")

# Initialize webcam
cap = cv2.VideoCapture(0)
print("Press key '1' to stop attendance scan.")

# Create or load Excel file
if not os.path.exists(attendance_file):
    wb = Workbook()
    ws = wb.active
    ws.title = "Attendance"
    ws.append(["Name", "Date", "Time", "Status"])
    wb.save(attendance_file)

# Function to mark attendance
def mark_attendance(name):
    wb = load_workbook(attendance_file)
    ws = wb.active
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    # Check if already marked today
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[0] == name and row[1] == date:
            return  # Already marked

    ws.append([name, date, time, "Present"])
    wb.save(attendance_file)
    print(f"✅ {name} marked present at {time}")

# Track who was marked present
present_names = set()

# Start live recognition
while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    faces = face_recognition.face_locations(rgb_small)
    encodes = face_recognition.face_encodings(rgb_small, faces)

    for encode_face, face_loc in zip(encodes, faces):
        matches = face_recognition.compare_faces(known_encodings, encode_face)
        face_dist = face_recognition.face_distance(known_encodings, encode_face)
        match_index = np.argmin(face_dist)

        if matches[match_index]:
            name = names[match_index].upper()
            if name not in present_names:
                mark_attendance(name)
                present_names.add(name)
            else:
                name = "UNKNOWN"
                

            # Draw rectangle and name
            y1, x2, y2, x1 = face_loc
            y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(frame, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)

    cv2.imshow("Attendance System", frame)

    # Stop scanning when key '1' is pressed
    if cv2.waitKey(1) & 0xFF == ord('1'):
        print("🛑 Attendance scanning stopped by user.")
        break

cap.release()
cv2.destroyAllWindows()

# Mark absent students
wb = load_workbook(attendance_file)
ws = wb.active
today = datetime.now().strftime("%Y-%m-%d")
for name in names:
    if name.upper() not in present_names:
        ws.append([name.upper(), today, "-", "Absent"])
        print(f"❌ {name} marked absent.")

wb.save(attendance_file)
print(f"✅ Attendance saved to {attendance_file}")
