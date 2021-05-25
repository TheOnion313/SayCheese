from cv2 import VideoCapture
from imutils.face_utils import shape_to_np
import cv2
import dlib
from sys import argv


def main():
    global INDEX, COLOR, RADIUS, PORT
    if "--index" in argv:
        INDEX = True

    if "--color" in argv:
        COLOR = tuple(argv[argv.index("--color") + 1].split(","))

    if "--radius" in argv:
        RADIUS = argv[argv.index("--radius") + 1]

    if "--port" in argv:
        PORT = argv[argv.index("--port") + 1]

    camera = None

    if len(argv) <= 1 or not argv[1].endswith(
            (".mp4", ".mov", ".wmv", ".avi", ".avchd", ".flv", ".f4v", ".swf", ".webm", ".html5", "mpeg-2", ".mkv")):
        camera = cv2.VideoCapture(int(PORT))
    else:
        camera = cv2.VideoCapture(argv[1])

    cv2.namedWindow("SayCheese")

    shape_predictor = "/home/the_onion313/Desktop/SayCheese/shape_predictor_68_face_landmarks.dat"
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(shape_predictor)

    ok = camera.read()[0]
    while ok:
        global frame
        ok, frame = camera.read()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rect = detector(gray, 0)

        circles = None

        if len(rect) > 0:
            # global frame
            rect = rect[0]
            shape = predictor(gray, rect)
            circles = shape_to_np(shape)

            for i, circle in enumerate(circles):
                # global frame
                frame = cv2.circle(frame, tuple(circles[i]), RADIUS, COLOR)

        cv2.imshow("SayCheese", frame)
        k = cv2.waitKey(1)
        if k != -1:
            if k in [ord(i) for i in 'qQ/']:
                cv2.destroyAllWindows()
                break


if __name__ == '__main__':
    global INDEX, COLOR, RADIUS, PORT
    INDEX = True
    COLOR = (180, 228, 236)
    RADIUS = 0
    PORT = 0

    main()
