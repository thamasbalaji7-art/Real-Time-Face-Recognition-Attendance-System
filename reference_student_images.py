import cv2
import os
from datetime import datetime

# Create folder for saving reference images
save_path = "reference_images"
if not os.path.exists(save_path):
    os.makedirs(save_path)

# Ask user details
name = input("Enter student name: ").strip()
reg_no = input("Enter register number: ").strip()

# Start webcam
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Error: Cannot open camera.")
    exit()

print("\nPress 'SPACE' to capture the image.")
print("Press 'ESC' to exit without saving.\n")

while True:
    ret, frame = cam.read()
    if not ret:
        print("Failed to capture image.")
        break

    # Display the video feed
    cv2.imshow("Press SPACE to Capture", frame)

    key = cv2.waitKey(1)
    if key % 256 == 27:  # ESC pressed
        print("Closing without saving.")
        break
    elif key % 256 == 32:  # SPACE pressed
        # Get current date and time
        now = datetime.now()
        date_time = now.strftime("%Y-%m-%d_%H-%M-%S")

        # Create filename
        filename = f"{reg_no}_{name}_{date_time}.jpg"
        filepath = os.path.join(save_path, filename)

        # Save the captured image
        cv2.imwrite(filepath, frame)
        print(f"\n✅ Image saved as: {filepath}")
        break

# Release camera and close window
cam.release()
cv2.destroyAllWindows()