import math
from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Rastrigin(BaseFunction):
    name = "rastrigin"
    label = "Растригин"
    parameters = []

    def evaluate(self, x, y):
        return 20 + x ** 2 - 10 * math.cos(2 * math.pi * x) + y ** 2 - 10 * math.cos(2 * math.pi * y)

    def gradient(self, x, y):
        return 0, 0

    def hessian(self):
        return [[0, 0], [0, 0]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

Factory.factory_function(Rastrigin())