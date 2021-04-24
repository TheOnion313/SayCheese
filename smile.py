from cv2 import VideoCapture
from imutils import face_utils
from math import dist

import imutils
import numpy as np
import time
import dlib
import cv2

FACE_IDX = (48, 68)

shape_predictor = "./shape_predictor_68_face_landmarks.dat"
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(shape_predictor)
(mStart, mEnd) = FACE_IDX

REPS = 0
SMILE = False
SMILE_MARK = False
SMILE_TIMESTAMP = -1

SMILE_NOT_TEETH = 0.3
SMILE_TEETH = 0.45


def MAR(mouth):
    d3_9 = dist(mouth[3], mouth[9])
    d2_10 = dist(mouth[2], mouth[10])
    d4_8 = dist(mouth[4], mouth[8])

    avg_d = (d3_9 + d2_10 + d4_8) / 3
    horizontal_d = dist(mouth[0], mouth[6])

    return avg_d / horizontal_d


camera = VideoCapture(2)
file_stream = False
cv2.namedWindow('SayCheese', cv2.WINDOW_NORMAL)

ok = camera.read()[0]
while ok:
    ok, frame = camera.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 0)

    mar = 0
    for rect in rects:
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)
        mouth = shape[mStart:mEnd]
        mar = MAR(mouth)

        if mar <= SMILE_NOT_TEETH or mar > SMILE_TEETH:
            print(SMILE_TIMESTAMP - time.time())
            if not SMILE:
                SMILE_TIMESTAMP = time.time()
                SMILE = True
            elif time.time() - SMILE_TIMESTAMP > 0.7 and not SMILE_MARK:
                REPS += 1
                SMILE_MARK = True

        else:
            SMILE = False
            SMILE_MARK = False

        mouth_hull = cv2.convexHull(mouth)
        cv2.drawContours(frame, [mouth_hull], -1, (0, 255, 0), 1)

    cv2.putText(frame, f"repetitions: {REPS}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f"MAR: {mar}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    key = cv2.waitKey(1)
    if key & 0xFF == ord("q"):
        break

    cv2.imshow('SayCheese', frame)

cv2.destroyAllWindows()
