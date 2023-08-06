import flask_socketio
import threading
import difflib
import flask
import time
import cv2

class MutableString:
    def __init__(self, string: str):
        self.string = string
        self.changes = "text" + self.string
    
    def update(self, string: str):
        modifs = ""
        for i,s in enumerate(difflib.ndiff(string, self.string)):
            if s[0] == ' ': continue
            if s[0] == '+':
                modifs += f"+{i}:{s[2]};"
            elif s[0] == '-':
                modifs += f"-{i}:{s[2]};"
        if len(modifs) < string:
            self.changes = "diff" + modifs
        else:
            self.changes = "text" + string
    
    def get_updates(self):
        return self.changes

class VideoObject:
    def __init__(self, webapp: flask.Flask, source: cv2.VideoCapture):
        self.webapp = webapp
        self.io = flask_socketio.SocketIO(self.webapp)
        self.source = source
        self.fps = self.source.get(5)
        self.still_runnning = threading.Event()
        self.old = ""
    
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

from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
from time import sleep

app = Flask(__name__)
io = SocketIO(app)


@app.route("/")
def index():
    return render_template("texts.html", content=get_file())


def get_file(loop = False, io: SocketIO = None):
    def read():
        with open("textfile.txt", "rb") as f:
            data = f.read()
        return data

    old = read()
    while loop:
        current = read()
        if current != old:
            io.emit("text", read().decode("utf-8"))
            old = current
        sleep(1)

    return read().decode("utf-8")


if __name__ == "__main__":
    Thread(target=lambda: get_file(loop=True, io=io)).start()
    io.run(app, debug=True)