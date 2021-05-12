from detect_smile import DetectSmile
from cv2 import VideoCapture
import cv2
import dlib
from typing import Iterable
import time


def main(smile_min, eye_mouth_min):
    smile = DetectSmile(smile_min, eye_mouth_min)

    camera = VideoCapture(0)
    cv2.namedWindow("SayCheese")

    counter = 0
    reps = 0
    reset = True

    shape_predictor = "./shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    ok = camera.read()[0]
    while ok:
        print(counter)
        ok, frame = camera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = detector(gray, 0)

        if len(rect) > 0:
            rect = rect[0]
            shape = predictor(gray, rect)

            relations = smile.relations_from_encoding(shape)

            out = smile(shape)

            if out:
                counter += 1
            else:
                reset = True
                counter = 0

            if counter > 20 and reset:
                counter = 0
                reps += 1
                reset = False

            frame1 = cv2.putText(frame, str(reps), (550, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), thickness=2)
            frame = cv2.putText(frame1, str(relations)[:8], (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0),
                                thickness=2)
        cv2.imshow("SayCheese", frame)
        k = cv2.waitKey(1)
        if k != -1:
            if k in [ord(i) for i in 'qQ/']:
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    main()
