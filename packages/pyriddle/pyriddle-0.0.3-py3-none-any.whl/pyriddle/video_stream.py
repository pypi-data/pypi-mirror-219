import threading
import flask
import time
import cv2

class VideoObject:
    def __init__(self, webapp: flask.Flask, source: cv2.VideoCapture):
        self.webapp = webapp
        self.source = source
        self.fps = self.source.get(5)
        self.still_runnning = threading.Event()
    
    def read_video(self, stop_condition = None):
        fps = self.source.get(5) # 5 = CAP_PROP_FPS => Nb of frames / second

        while not self.still_runnning.is_set():
            if type(stop_condition) == threading.Event and stop_condition.is_set():
                break
            flag, npframe = self.source.read()
            if not flag:
                self.still_runnning.set()
                continue
            ret, buffer = cv2.imencode('.jpg', npframe)
            if not ret:
                self.still_runnning.set()
                continue
            frame = buffer.tobytes()
            yield (b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" +
                   frame +
                   b"\r\n")
            time.sleep(1 / fps)
    
    def stream(self, stop_condition = None):
        return flask.Response(self.read_video(stop_condition),
            mimetype="multipart/x-mixed-replace; boundary=frame")