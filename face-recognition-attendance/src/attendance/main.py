import argparse
import logging
import cv2
import face_recognition
from . import storage
from . import recognition
from . import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%H:%M:%S'
)

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="attendance",
        description="Face Recognition Attendance System (starter CLI)",
    )

    sub = parser.add_subparsers(dest="cmd", required=False)

    enroll = sub.add_parser("enroll", help="Enroll a new face using webcam")
    enroll.add_argument("name", help="Person's name")

    sub.add_parser("recognize", help="Recognize face from webcam and mark attendance")

    sub.add_parser("list", help="List attendance entries (today)")

    args = parser.parse_args()

    if args.cmd == "enroll":
        success = recognition.capture_face_encoding(args.name)
        if not success:
            logging.error("Enrollment failed.")
    elif args.cmd == "recognize":
        # Load known faces
        known_encodings, known_names = recognition.load_known_faces()
        
        if not known_encodings:
            logging.warning("No enrolled faces found. Use 'enroll' command first.")
            return
        
        video_capture = cv2.VideoCapture(config.CAMERA_INDEX)
        
        if not video_capture.isOpened():
            logging.error("Could not open webcam")
            return
        
        logging.info("Looking for faces... Press ESC to exit.")
        recognized_today = set()
        frame_count = 0
        current_name = "Unknown"
        
        while True:
            ret, frame = video_capture.read()
            if not ret:
                break
            
            frame_count += 1
            
            # Process every Nth frame for better performance
            if frame_count % config.FRAME_SKIP == 0:
                current_name = recognition.recognize_from_frame(frame, known_encodings, known_names)
                
                # Mark attendance if recognized and not already marked today
                if current_name != "Unknown" and current_name not in recognized_today:
                    if not storage.is_attendance_marked_today(current_name):
                        storage.mark_attendance(current_name)
                        logging.info(f"Attendance marked for: {current_name}")
                    recognized_today.add(current_name)
            
            # Draw rectangle and name on frame
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face_locations = face_recognition.face_locations(rgb_frame)
            
            for (top, right, bottom, left) in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), config.RECTANGLE_COLOR, config.RECTANGLE_THICKNESS)
                cv2.putText(frame, current_name, (left, top - 10), config.FONT, config.FONT_SCALE, config.RECTANGLE_COLOR, config.FONT_THICKNESS)
            
            cv2.imshow(config.WINDOW_NAME, frame)
            
            # ESC key to exit
            if cv2.waitKey(1) & 0xFF == 27:
                break
        
        video_capture.release()
        cv2.destroyAllWindows()
    elif args.cmd == "list":
        rows = storage.load_attendance()
        if not rows:
            logging.info("No attendance records found.")
        else:
            for r in rows:
                print(
                    f"{r.get('timestamp','')}\t{r.get('name','')}\t{r.get('status','')}"
                )
    else:
        parser.print_help()


if __name__ == "__main__":  # pragma: no cover
    main()
