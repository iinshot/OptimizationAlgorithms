from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Himmelblau(BaseFunction):
    name = "himmelblau"
    label = "Химмельблау"
    parameters = []

    def evaluate(self, x, y):
        return (x ** 2 + y - 11) ** 2 + (x + y ** 2 - 7) ** 2

    def gradient(self, x, y):
        grad_x = 4 * x * (x ** 2 + y - 11) + 2 * (x + y ** 2 - 7)
        grad_y = 2 * (x ** 2 + y - 11) + 4 * y * (x + y ** 2 - 7)
        return grad_x, grad_y

    def hessian(self):
        return [[0, 0], [0, 0]]

    def linear_coefs(self):
        return [0, 0]

    def constraints(self):
        return []

    def plot_bounds(self):
        return -6.0, 6.0

Factory.factory_function(Himmelblau())