
from abc import *


class Scrapper(metaclass=ABCMeta):

    def __init__(self):
        pass

    @abstractmethod
    def set_url(self, *args):
        pass

    @abstractmethod
    def scrapping(self, *args):
        pass