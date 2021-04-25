from typing import Iterable, Union

from detection import Detection
from math import dist
from imutils.face_utils import shape_to_np
import numpy as np

M_START, M_END = 48, 68


class DetectSmile(Detection):

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

    def calibrate(self, me: Union[Iterable[float], Iterable[Iterable[float]]]):
        assert type(me) == Iterable[float]

        self.relations = range(min(me), 10 ** 10)
