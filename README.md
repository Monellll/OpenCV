<<<<<<< HEAD
# Smart Attendance System by Face / Gesture 👩‍💻

A Python-based attendance system using OpenCV that automatically detects student presence through webcam and marks attendance using two modes:

## Features

- **Face Recognition Mode**: Detect and recognize student faces for attendance
- **Gesture Mode**: Detect raised hand gesture to mark attendance
- **Student Registration**: Register students with face data or ID
- **Attendance Logging**: Store attendance with timestamp in CSV and SQLite
- **Dashboard**: View attendance records with filtering options
- **Export**: Export attendance data to CSV/Excel formats

## Tech Stack

- Python 3.8+
- OpenCV (Computer Vision)
- face_recognition (Face Recognition)
- MediaPipe (Gesture Detection)
- Tkinter (GUI)
- SQLite (Database)
- Pandas (Data Processing)

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Project Structure

```
├── main.py                 # Main application entry point
├── face_recognition_module.py  # Face detection and recognition
├── gesture_detection.py   # Hand gesture detection
├── attendance_manager.py  # Attendance logging and management
├── dashboard.py           # GUI dashboard for viewing records
├── student_registration.py # Student registration system
├── data/
│   ├── faces/             # Stored face encodings
│   ├── attendance.csv     # CSV attendance log
│   └── attendance.db      # SQLite database
└── requirements.txt       # Project dependencies
```

## Usage

1. **Register Students**: Add student faces or IDs to the system
2. **Select Mode**: Choose between Face Recognition or Gesture Detection
3. **Mark Attendance**: System automatically detects and marks attendance
4. **View Records**: Use dashboard to view and export attendance data

## Modes

### Face Recognition Mode
- Detects faces in real-time
- Matches against registered student faces
- Automatically marks attendance when recognized

### Gesture Mode
- Detects raised hand gesture
- Prompts for student ID input
- Marks attendance upon gesture confirmation
=======
# OpenCV
Smart Attendance System using OpenCV and Python.
>>>>>>> a45273119ac13a26cfdc56aa150e1787a9459700
