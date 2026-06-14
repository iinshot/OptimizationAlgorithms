from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class SphereFunction(BaseFunction):
    name = "sphere"
    label = "Сфера"
    parameters = []

    def evaluate(self, x, y):
        return x ** 2 + y ** 2

    def gradient(self, x, y):
        return 2 * x, 2 * y

    def hessian(self):
        return [[2, 0], [0, 2]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

Factory.factory_function(SphereFunction())