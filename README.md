# AirCursor

AirCursor is a webcam-based hand tracking project that lets you move your mouse cursor with your index finger.

## Features

- Tracks your hand using MediaPipe
- Moves the cursor using your index fingertip
- Smooths cursor movement to reduce jitter
- Shows a webcam preview with hand landmarks drawn on top
- Flips the webcam view so it feels like a mirror

## Files

- `main.py` - starts the project
- `hand_cursor_connection.py` - turns hand movement into cursor movement
- `hand_tracking.py` - handles MediaPipe hand tracking
- `webcam_access.py` - handles webcam input and display

## Setup

Install the needed packages:

```bash
pip install opencv-python mediapipe pyautogui
```

Download the MediaPipe hand model:

```text
https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/1/hand_landmarker.task
```

Put the downloaded file next to `hand_tracking.py`:

```text
AirCursor/
  hand_landmarker.task
  hand_tracking.py
```

The model file is ignored by Git, so it needs to be downloaded locally.

## Run

```bash
python main.py
```

Press `q` while the webcam window is selected to quit.

## Notes

- Cursor movement uses hand landmark `8`, the index fingertip.
- `SMOOTH_AMOUNT` in `hand_cursor_connection.py` controls cursor smoothing.
- Lower smoothing values are steadier but slower.
- Higher smoothing values are faster but more shaky.
