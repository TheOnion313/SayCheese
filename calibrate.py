from cv2 import VideoCapture
from imutils import face_utils
from math import dist
from detection import Detection
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

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = detector(gray, 0)[0]
        shape = predictor(gray, rect)

        relations = gesture.relations_from_encoding(shape)

        if cv2.waitKey() & 0xFF == ord('y'):
            if dt_y == [] and type(relations) == Iterable:
                for i in relations:
                    dt_y.append([])

            if type(relations) == Iterable:
                for i in range(len(list(relations))):
                    dt_y[i].append(list(relations)[i])
            else:
                dt_y.append(relations)

        if cv2.waitKey() & 0xFF == ord('n'):
            if dt_n == [] and type(relations) == Iterable:
                for i in relations:
                    dt_n.append([])

            if type(relations) == Iterable:
                for i in range(len(list(relations))):
                    dt_n[i].append(list(relations)[i])
            else:
                dt_n.append(relations)

    return dt_y, dt_n

