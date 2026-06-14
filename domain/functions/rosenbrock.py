from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Rosenbrock(BaseFunction):
    name = "rosenbrock"
    label = "Розенброк"
    parameters = []

    def evaluate(self, x, y):
        return (1 - x) ** 2 + 100 * (y - x * x) ** 2

    def gradient(self, x, y):
        grad_x = -2 * (1 - x) - 400 * x * (y - x ** 2)
        grad_y = 200 * (y - x ** 2)
        return grad_x, grad_y

    def hessian(self):
        return [[0, 0], [0, 0]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

    def plot_bounds(self):
        return -100.0, 100.0

Factory.factory_function(Rosenbrock())