from pathlib import Path

import cv2
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
import mediapipe as mp
import webcam_access

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# MediaPipe returns 21 landmarks per hand. These pairs draw the hand skeleton.
HAND_CONNECTIONS = (
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (5, 9), (9, 10), (10, 11), (11, 12),
    (9, 13), (13, 14), (14, 15), (15, 16),
    (13, 17), (17, 18), (18, 19), (19, 20),
    (0, 17),
)


class HandTracker:
    def __init__(self, model_path="hand_landmarker.task"):
        model_path = Path(model_path)
        if not model_path.is_absolute():
            model_path = Path(__file__).with_name(model_path.name)

        if not model_path.exists():
            raise FileNotFoundError(
                f"Missing model file: {model_path}\n"
                "Download hand_landmarker.task and put it next to hand_tracking.py."
            )

        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=2,
        )

        self.landmarker = vision.HandLandmarker.create_from_options(options)
        self.frame_time_ms = 0

    def find_hands(self, frame):
        """Return MediaPipe hand results for one webcam frame."""
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        self.frame_time_ms += 1
        return self.landmarker.detect_for_video(mp_image, self.frame_time_ms)

    def draw_hands(self, frame, results):
        """Draw detected hands on the frame."""
        if not results.hand_landmarks:
            return frame

        for hand in results.hand_landmarks:
            points = self.landmarks_to_pixels(frame, hand)

            for start, end in HAND_CONNECTIONS:
                cv2.line(frame, points[start], points[end], (255, 0, 0), 2)

            for point in points:
                cv2.circle(frame, point, 4, (0, 255, 0), -1)

        return frame

    def process_frame(self, frame):
        """Find hands, draw them, and return the frame plus raw results."""
        results = self.find_hands(frame)
        frame = self.draw_hands(frame, results)
        return frame, results

    @staticmethod
    def landmarks_to_pixels(frame, hand_landmarks):
        """Convert MediaPipe's 0-1 landmark positions into screen pixels."""
        height, width, _ = frame.shape

        points = []
        for landmark in hand_landmarks:
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            points.append((x, y))

        return points

    def close(self):
        self.landmarker.close()


def main():
    tracker = None

    try:
        tracker = HandTracker()
        webcam = webcam_access.WebcamAccess(0)

        def on_frame(frame):
            frame, results = tracker.process_frame(frame)

            # Later, use results.hand_landmarks here for mouse/space controls.
            return frame

        webcam.run(on_frame, title="Hand Tracking")

    except (FileNotFoundError, RuntimeError) as error:
        print(error)

    finally:
        if tracker is not None:
            tracker.close()


if __name__ == "__main__":
    main()
