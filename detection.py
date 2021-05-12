from abc import ABC, abstractmethod, abstractclassmethod
from typing import Union, Tuple, Iterable

import cv2


class Detection(ABC):

    @abstractmethod
    def relations_from_encoding(self, encoding: Iterable[float]) -> Union[float, Iterable[float]]:
        pass

    @abstractmethod
    def detect(self, encoding: Iterable[Tuple[float]]) -> bool:
        pass

    def __call__(self, *args, **kwargs):
        return self.detect(*args, **kwargs)

    @abstractmethod
    def calibrate(self, me: Union[Iterable[float], Iterable[Iterable[float]]]):
        pass
