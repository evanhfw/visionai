import cv2

class RTSPStream:
    def __init__(self, url):
        self.cap = cv2.VideoCapture(url, cv2.CAP_FFMPEG)

    def read(self):
        return self.cap.read()

    def release(self):
        self.cap.release()
