from cv2 import VideoCapture
from imutils import face_utils
from math import dist

import test_smile
from detection import Detection
from detect_smile import DetectSmile
from typing import Union, Iterable

import imutils
import numpy as np
import time
import dlib
import cv2


def calibrate(gesture: Detection) -> Union[Iterable[float], Iterable[Iterable[float]]]:
    camera = VideoCapture(0)
    cv2.namedWindow('SayCheese')

    dt_y = []
    dt_n = []
    shape_predictor = "./shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    ok = camera.read()[0]
    while ok:
        ok, frame = camera.read()

        k = cv2.waitKey(1)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = detector(gray, 0)
        if len(rect) > 0:
            rect = rect[0]
            shape = predictor(gray, rect)

            relations = gesture.relations_from_encoding(shape)

            frame = cv2.putText(frame, str(relations), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

            for i, circle in enumerate(face_utils.shape_to_np(shape)):
                print(circle)
                cv2.circle(frame, tuple(circle), radius=3, color=(0, 0, 255), thickness=-1)
                cv2.putText(frame, str(i), tuple(circle), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0))
            cv2.imshow("SayCheese", frame)
            if k & 0xFF == ord('y'):
                if dt_y == [] and type(relations) == Iterable:
                    for i in relations:
                        dt_y.append([])

                if type(relations) == Iterable:
                    for i in range(len(list(relations))):
                        dt_y[i].append(list(relations)[i])
                else:
                    dt_y.append(relations)

            if k & 0xFF == ord('n'):
                if dt_n == [] and type(relations) == Iterable:
                    for i in relations:
                        dt_n.append([])

                if type(relations) == Iterable:
                    for i in range(len(list(relations))):
                        dt_n[i].append(list(relations)[i])
                else:
                    dt_n.append(relations)

        if k & 0xFF == ord('q'):
            break

    return dt_y, dt_n


if __name__ == '__main__':
    smile = DetectSmile(0, 0)

    smile.calibrate(calibrate(smile))
    print(smile.smile_min)
    test_smile.main(smile.smile_min, smile.eye_mouth_min)
