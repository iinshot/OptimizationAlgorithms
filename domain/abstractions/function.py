from abc import ABC, abstractmethod

class BaseFunction(ABC):
    name: str
    label: str
    parameters: dict

    @abstractmethod
    def evaluate(self, x, y):
        pass

    def visualize(self, x, y):
        return self.evaluate(x, y)