"""Configuration settings for the attendance system."""
import os

# Paths
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "attendance.csv")
ENCODINGS_PATH = os.path.join(DATA_DIR, "face_encodings.pkl")

# Recognition settings
FACE_RECOGNITION_TOLERANCE = 0.6
FRAME_SKIP = 2  # Process every Nth frame for better performance

# Camera settings
CAMERA_INDEX = 0

# Display settings
WINDOW_NAME = "Face Recognition Attendance"
RECTANGLE_COLOR = (0, 255, 0)  # Green
RECTANGLE_THICKNESS = 2
FONT = 1  # cv2.FONT_HERSHEY_SIMPLEX
FONT_SCALE = 0.9
FONT_THICKNESS = 2
