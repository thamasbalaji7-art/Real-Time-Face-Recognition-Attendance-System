# Face Recognition Attendance System

A webcam-based attendance system that recognizes registered students' faces and automatically marks them present in a timestamped Excel sheet.

## Project Structure

```
├── reference_student_images.py   # Capture and save a student's reference photo
├── attendance_marking_code.py    # Run live face recognition and mark attendance
├── reference_images/             # Auto-created folder storing captured photos
└── Attendance-<Hour> O'Clock.xlsx  # Auto-generated attendance sheet per run
```

## How It Works

1. Run `reference_student_images.py` once per student to capture and save their face photo.
2. Run `attendance_marking_code.py` to start the webcam feed — it recognizes faces against the saved photos and marks each matched student "Present" in an Excel file, then marks everyone else "Absent" when the scan ends.

## Prerequisites

- **Python 3.9–3.11** (face_recognition / dlib do not yet reliably support 3.12+). Check your version with:
  ```
  python --version
  ```
- **VS Code** with the Python extension installed
- **Windows users only:** install **CMake** and **Visual Studio Build Tools (C++ build tools workload)** before installing `dlib` — this is the single most common installation failure. See step 3 below.

## Installation (VS Code)

1. **Open the project folder in VS Code**, then open a new terminal: `Terminal > New Terminal`.

2. **Create and activate a virtual environment** (keeps these libraries isolated from your system Python):
   ```
   python -m venv venv
   ```
   Windows:
   ```
   venv\Scripts\activate
   ```
   macOS/Linux:
   ```
   source venv/bin/activate
   ```
   In VS Code, also select this environment as your interpreter: `Ctrl+Shift+P` → `Python: Select Interpreter` → choose the `venv` one.

3. **Install CMake and dlib's build dependencies (Windows only — skip on macOS/Linux):**
   - Install [CMake](https://cmake.org/download/) and make sure to check "Add CMake to system PATH" during setup.
   - Install [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/), and in the installer select the **"Desktop development with C++"** workload.
   - Restart VS Code after both installs so the terminal picks up the updated PATH.

4. **Install the required Python libraries:**
   ```
   pip install opencv-python face_recognition numpy openpyxl
   ```
   This step can take several minutes the first time, since `face_recognition` builds `dlib` from source. If it fails on Windows, double check step 3 was completed, then try again.

   If `pip install face_recognition` still fails on Windows after step 3, install a prebuilt dlib wheel instead:
   ```
   pip install dlib-binary
   pip install face_recognition
   ```

5. **Verify the install** by running:
   ```
   python -c "import cv2, face_recognition, numpy, openpyxl; print('All libraries installed correctly')"
   ```

## Usage

1. Capture a reference photo for each student:
   ```
   python reference_student_images.py
   ```
   Enter the student's name and register number when prompted, then press `SPACE` to capture (or `ESC` to cancel).

2. Run attendance marking:
   ```
   python attendance_marking_code.py
   ```
   Press `1` to stop the scan. An Excel file named `Attendance-<Hour> O'Clock.xlsx` will be created/updated in the project folder with each student's status.

## Troubleshooting

| Issue | Fix |
|---|---|
| `pip install face_recognition` fails with a CMake/dlib build error | Complete step 3 (CMake + VS Build Tools), restart the terminal, and retry |
| Webcam doesn't open (`cap.isOpened()` is False) | Check no other app is using the webcam, and that VS Code/terminal has camera permission (Windows: Settings > Privacy > Camera) |
| No faces recognized / everyone shows as unknown | Ensure `reference_images/` has at least one clear, well-lit photo per student, and that the filename format matches what `attendance_marking_code.py` expects |
| `ModuleNotFoundError` for any library | Confirm the `venv` is activated (you should see `(venv)` in the terminal prompt) before running `pip install` or the script |

## requirements.txt

For convenience, you can also save this as `requirements.txt` in the repo and install everything with `pip install -r requirements.txt`:

```
opencv-python
face_recognition
numpy
openpyxl
```
