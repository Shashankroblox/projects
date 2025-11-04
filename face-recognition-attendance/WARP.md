# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Commands

Setup (macOS/Linux):
- Create venv: `python3 -m venv .venv && source .venv/bin/activate`
- Install package: `pip install -e .`

Run the CLI:
- Help: `attendance --help`
- Enroll face: `attendance enroll "Alice"`
- Recognize faces: `attendance recognize`
- List attendance: `attendance list`

Build/Lint/Test:
- Build: Installed via `pip install -e .` using pyproject.toml
- Lint/Format: not configured in this repo.
- Tests: no test suite/config present.

## High-level architecture

- Package layout: `src/attendance/` (src-layout Python package named `attendance`). The CLI is installed as `attendance` command via pyproject.toml.
- CLI (`main.py`): argparse-based entrypoint with subcommands:
  - `enroll <name>` captures a face via webcam and saves encoding.
  - `recognize` runs real-time face recognition and marks attendance automatically.
  - `list` reads CSV and prints timestamp/name/status rows.
- Storage (`storage.py`):
  - Ensures `data/attendance.csv` exists with header.
  - `mark_attendance(name, status="Present")` appends ISO-8601 timestamped rows.
  - `is_attendance_marked_today(name)` checks for duplicate daily entries.
  - `load_attendance()` returns rows as dicts.
- Recognition (`recognition.py`):
  - `load_known_faces()` loads face encodings from pickle file.
  - `save_face_encoding(name, encoding)` saves new encodings.
  - `recognize_from_frame(frame, encodings, names)` returns recognized name or "Unknown".
  - `capture_face_encoding(name)` interactive webcam capture for enrollment.
- Config (`config.py`): Centralized configuration for paths, recognition settings, camera, and display options.

Data and side effects:
- CSV is stored at `data/attendance.csv` (created automatically on first write/read).

## Notes from README

- Dependencies include `opencv-python` and `face-recognition`; these may require native/system toolchains to install successfully on some machines.
