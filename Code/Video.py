import cv2

class Video(object):
    def __init__(self):
        self.cap = None
        self.status = False

    def start(self):
        self.cap = cv2.VideoCapture(0)

    def stop(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        return frame
