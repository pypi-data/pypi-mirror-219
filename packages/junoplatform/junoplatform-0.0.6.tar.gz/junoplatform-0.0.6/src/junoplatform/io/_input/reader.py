from abc import ABC, abstractmethod
from typing import List

from datetime import datetime


class Reader(ABC):
    @abstractmethod
    def read(self, keys: List[str], start: datetime|None, end: datetime|None, num:int|None):
        pass