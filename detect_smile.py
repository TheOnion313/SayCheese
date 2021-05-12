from typing import Iterable, Union, Tuple

from detection import Detection
from math import dist
from imutils.face_utils import shape_to_np
import numpy as np

M_START, M_END = 48, 68


class DetectSmile(Detection):

    def __init__(self, smile_min):
        self.smile_min = smile_min

    def _MAR(self, mouth):
        d3_9 = dist(mouth[3], mouth[9])
        d2_10 = dist(mouth[2], mouth[10])
        d4_8 = dist(mouth[4], mouth[8])

        avg_d = (d3_9 + d2_10 + d4_8) / 3
        horizontal_d = dist(mouth[0], mouth[6])

        return avg_d / horizontal_d

    def relations_from_encoding(self, encoding: Iterable[float]) -> Union[float, Iterable[float]]:
        shape = shape_to_np(encoding)
        mouth = shape[M_START:M_END]

        mar = self._MAR(mouth)
        return mar

    def detect(self, encoding: Iterable[Tuple[float]]) -> bool:
        return self.relations_from_encoding(encoding) > self.smile_min

    def calibrate(self, me: Union[
                        Tuple[Iterable[float], Iterable[float]],
                        Tuple[Iterable[Iterable[float]], Iterable[Iterable[float]]]
                        ]) -> None:
        # assert type(me) == Tuple[Iterable[float], Iterable[float]]

        self.smile_min = min(me[0])
