
from abc import *


class Traveler(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def traveling(self, target):
        pass