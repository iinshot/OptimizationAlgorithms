from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class InverseSphere(BaseFunction):
    name = "inverse_sphere"
    label = "Обратная сфера"
    parameters = []

    def evaluate(self, x, y):
        return -(x**2 + y**2)

    def gradient(self, x, y):
        return -2*x, -2*y

    def hessian(self):
        return [[0, 0], [0, 0]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

    def plot_bounds(self):
        return -5.0, 5.0

Factory.factory_function(InverseSphere())