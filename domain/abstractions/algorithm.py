from abc import ABC, abstractmethod

class BaseAlgorithm(ABC):
    name: str
    label: str
    parameters: dict

    @abstractmethod
    def optimize(self, function, params: dict) -> dict:
        pass