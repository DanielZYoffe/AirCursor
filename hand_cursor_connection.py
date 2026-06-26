import pyautogui

from hand_tracking import HandTracker
from webcam_access import WebcamAccess


INDEX_FINGER_TIP = 8
SMOOTH_AMOUNT = 0.1


class HandCursor:
    def __init__(self):
        self.tracker = HandTracker()
        self.screen_width, self.screen_height = pyautogui.size()
        self.smooth_amount = SMOOTH_AMOUNT
        self.cursor_x, self.cursor_y = pyautogui.position()

    def move_cursor(self, results):
        if not results.hand_landmarks:
            return

        hand = results.hand_landmarks[0]
        index_tip = hand[INDEX_FINGER_TIP]

        x = int(index_tip.x * self.screen_width)
        y = int(index_tip.y * self.screen_height)

        self.cursor_x += (x - self.cursor_x) * self.smooth_amount
        self.cursor_y += (y - self.cursor_y) * self.smooth_amount

        pyautogui.moveTo(self.cursor_x, self.cursor_y)

    def process_frame(self, frame):
        frame, results = self.tracker.process_frame(frame)
        self.move_cursor(results)
        return frame

    def close(self):
        self.tracker.close()


def main():
    cursor = None

    try:
        cursor = HandCursor()
        webcam = WebcamAccess(0, fps=30)
        webcam.run(cursor.process_frame, title="Hand Cursor")
    finally:
        if cursor is not None:
            cursor.close()


if __name__ == "__main__":
    main()
