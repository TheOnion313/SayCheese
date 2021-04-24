from abc import ABC, abstractmethod, abstractclassmethod
from typing import Union, Tuple, Iterable


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
        return all(map(lambda i: out[i][0] <= inp <= out[i][-1], range(len(inp) if type(inp) == Iterable else 1)))

    def __call__(self, encoding):
        return self.detect(encoding)
