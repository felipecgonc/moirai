# file: test.py
import cv2
import time
from datetime import datetime, timedelta
import requests
from pydarknet import Detector, Image
from videocaptureasync import VideoCaptureAsync

def main(width=640, height=360, k=False):
    last_detected = datetime(1990,1,1)
    if k:
        cap = VideoCaptureAsync(0)
    else:
        cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    if k:
        cap.start()
    t0 = time.time()
    i = 0
    net = Detector(bytes("cfg/yolo-lite.cfg", encoding="utf-8"), bytes("moirai.weights", encoding="utf-8"), 0,
                   bytes("obj.data", encoding="utf-8"))
    while True:
        r, frame = cap.read()
        if r:
            dark_frame = Image(frame)
            results = net.detect(dark_frame)
            del dark_frame

            for cat, score, bounds in results:
                x, y, w, h = bounds
                cv2.rectangle(frame, (int(x-w/2),int(y-h/2)),(int(x+w/2),int(y+h/2)),(255,0,255))
            if len(results) > 0:
                if datetime.now() > last_detected + timedelta(seconds=6):
                    last_detected = datetime.now()
                    prob = results[0][1]
                    requests.post('http://192.168.6.219:8080/area/alert', data={"cam_id": 1, "prob": prob})
        cv2.imshow('Frame', frame)
        cv2.waitKey(1) & 0xFF
    if k:
        cap.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main(width=640, height=360, k=True)
