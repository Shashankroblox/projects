"""Face recognition logic using face_recognition library and OpenCV."""

import os
import pickle
from typing import List, Tuple, Any
import face_recognition
import cv2
import numpy as np
from . import config


def load_known_faces() -> Tuple[List[Any], List[str]]:
    """Load known face encodings and labels from disk."""
    if not os.path.exists(config.ENCODINGS_PATH):
        return [], []
    
    with open(config.ENCODINGS_PATH, "rb") as f:
        data = pickle.load(f)
    
    return data.get("encodings", []), data.get("names", [])


def save_face_encoding(name: str, encoding: Any) -> None:
    """Save a face encoding for a person."""
    os.makedirs(config.DATA_DIR, exist_ok=True)
    
    # Load existing data
    encodings, names = load_known_faces()
    
    # Add new encoding
    encodings.append(encoding)
    names.append(name)
    
    # Save back
    with open(config.ENCODINGS_PATH, "wb") as f:
        pickle.dump({"encodings": encodings, "names": names}, f)


def recognize_from_frame(frame: Any, known_encodings: List[Any], known_names: List[str]) -> str:
    """Recognize a face in a frame, return best-match name or 'Unknown'."""
    if not known_encodings:
        return "Unknown"
    
    # Convert BGR (OpenCV) to RGB (face_recognition)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
    
    if not face_encodings:
        return "Unknown"
    
    # Use the first detected face
    face_encoding = face_encodings[0]
    
    # Compare with known faces
    matches = face_recognition.compare_faces(known_encodings, face_encoding, tolerance=config.FACE_RECOGNITION_TOLERANCE)
    face_distances = face_recognition.face_distance(known_encodings, face_encoding)
    
    if True in matches:
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            return known_names[best_match_index]
    
    return "Unknown"


def capture_face_encoding(name: str) -> bool:
    """Capture a face from webcam and save its encoding."""
    video_capture = cv2.VideoCapture(config.CAMERA_INDEX)
    
    if not video_capture.isOpened():
        print("Error: Could not open webcam")
        return False
    
    print(f"\nCapturing face for: {name}")
    print("Position your face in the camera and press SPACE to capture, or ESC to cancel...")
    
    encoding = None
    
    while True:
        ret, frame = video_capture.read()
        if not ret:
            break
        
        # Display the frame
        cv2.imshow(f"Capture Face - {name}", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        # ESC key to cancel
        if key == 27:
            print("Cancelled.")
            break
        
        # SPACE key to capture
        if key == 32:
            print("Processing...")
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
            
            if face_encodings:
                encoding = face_encodings[0]
                save_face_encoding(name, encoding)
                print(f"Successfully enrolled: {name}")
                break
            else:
                print("No face detected. Try again...")
    
    video_capture.release()
    cv2.destroyAllWindows()
    
    return encoding is not None
