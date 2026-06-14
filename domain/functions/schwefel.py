from domain.abstractions.function import BaseFunction
from domain.factory import Factory
import math

class Schwefel(BaseFunction):
    name = "schwefel"
    label = "Швефель"
    parameters = []

    def evaluate(self, x, y):
        return 418.9829 * 2 - x * math.sin(math.sqrt(abs(x))) - y * math.sin(math.sqrt(abs(y)))

    def gradient(self, x, y):
        return 0, 0

    def hessian(self):
        return [[0, 0], [0, 0]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

    def plot_bounds(self):
        return -500.0, 500.0

Factory.factory_function(Schwefel())