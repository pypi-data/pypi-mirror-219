from abc import ABC


class Metric(ABC):

    def __init__(self, name: str):
        self.name: str = name
