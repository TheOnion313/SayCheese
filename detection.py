from abc import ABC, abstractmethod, abstractclassmethod
from typing import Union, Tuple, Iterable

import cv2


class Detection(ABC):

    def __init_subclass__(cls, **kwargs):
        assert 'relations' in kwargs.keys()
        cls.relations = kwargs['relations']

    def __iter__(self):
        return self.relations

    @abstractmethod
    def relations_from_encoding(self, encoding: Iterable[float]) -> Union[float, Iterable[float]]:
        pass

    def detect(self, encoding: Iterable[float]) -> bool:
        inp = self.relations_from_encoding(encoding)
        out = self.relations

        if type(inp) == Iterable:
            return all(map(lambda i: inp[i] in out[i], range(len(inp))))
        return inp in out

    def __call__(self, encoding):
        return self.detect(encoding)

    @abstractmethod
    def calibrate(self, me: Union[Iterable[float], Iterable[Iterable[float]]]):
        pass
