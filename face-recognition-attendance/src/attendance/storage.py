import csv
from datetime import datetime, date
from typing import List, Dict
from . import config


def _ensure_storage() -> None:
    import os
    os.makedirs(config.DATA_DIR, exist_ok=True)
    if not os.path.exists(config.CSV_PATH):
        with open(config.CSV_PATH, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["timestamp", "name", "status"])
            writer.writeheader()


def is_attendance_marked_today(name: str) -> bool:
    """Check if attendance is already marked for the person today."""
    _ensure_storage()
    today = date.today().isoformat()
    
    with open(config.CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            timestamp = row.get("timestamp", "")
            if timestamp.startswith(today) and row.get("name") == name:
                return True
    return False


def mark_attendance(name: str, status: str = "Present") -> None:
    """Mark attendance for a person. Returns True if marked, False if already marked today."""
    _ensure_storage()
    
    with open(config.CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "name", "status"])
        writer.writerow({
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "name": name,
            "status": status,
        })


def load_attendance() -> List[Dict[str, str]]:
    """Load all attendance records."""
    _ensure_storage()
    with open(config.CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)
