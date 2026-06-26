import cv2

class WebcamAccess:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = cv2.VideoCapture(camera_index)

    def is_opened(self):
        return self.cap is not None and self.cap.isOpened()

    def read_frame(self):
        if self.cap is None:
            return False, None
        return self.cap.read()

    def release(self):
        if self.cap is not None:
            self.cap.release()
            self.cap = None

    def show_frame(self, title, frame):
        cv2.imshow(title, frame)

    @staticmethod
    def should_exit(key_code):
        return (key_code & 0xFF) == ord("q")

    def run(self, frame_callback, title="Webcam"):
        if not self.is_opened():
            raise RuntimeError("Error: Could not open webcam")

        while True:
            ret, frame = self.read_frame()
            if not ret:
                print("Failed to get frame")
                break

            output = frame_callback(frame)
            self.show_frame(title, output)

            if self.should_exit(cv2.waitKey(1)):
                break

        self.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    def identity(frame):
        return frame

    webcam = WebcamAccess(0)
    webcam.run(identity)
