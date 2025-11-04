# Face Recognition Attendance System

A Python-based face recognition attendance system with webcam support. Features automatic face enrollment, real-time recognition, and CSV-based attendance logging.

## Features

- 👤 **Face Enrollment**: Capture and store face encodings via webcam
- 🎥 **Real-time Recognition**: Identify enrolled faces from live video feed
- 📊 **Attendance Tracking**: Automatic daily attendance logging to CSV
- ⚡ **Performance Optimized**: Frame skipping and configurable settings
- 🚫 **Duplicate Prevention**: Prevents multiple attendance marks per person per day

## Installation

1. **Create a virtual environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install the package**:
   ```bash
   pip install -e .
   ```

## Usage

### Enroll a New Face
```bash
attendance enroll "John Doe"
```
Press **SPACE** to capture, **ESC** to cancel.

### Run Face Recognition
```bash
attendance recognize
```
Press **ESC** to exit. Attendance is automatically marked when a face is recognized.

### List Attendance Records
```bash
attendance list
```

### View All Commands
```bash
attendance --help
```

## Project Structure

- `src/attendance/` — Main package
  - `main.py` — CLI entrypoint
  - `recognition.py` — Face recognition logic
  - `storage.py` — CSV-based attendance storage
  - `config.py` — Configuration settings
- `data/` — Generated data directory
  - `attendance.csv` — Attendance records
  - `face_encodings.pkl` — Stored face encodings

## Configuration

Edit `src/attendance/config.py` to customize:
- Recognition tolerance
- Frame skip rate (performance)
- Camera index
- Display settings

## Notes

- **Dependencies**: Face recognition requires native libraries (dlib, CMake). Installation may require system toolchains.
- **macOS**: You may need to install CMake: `brew install cmake`
- **Linux**: Install dlib dependencies: `sudo apt-get install build-essential cmake`
- **First Run**: The `data/` directory is created automatically on first use.
