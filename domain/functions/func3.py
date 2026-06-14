from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Func3(BaseFunction):
    name = "Func3"
    label = "x₁ + 2x₂ − x₂²"
    parameters = []

    def visualize(self, x, y):
        return x + 2 * y - y ** 2

    def evaluate(self, x, y):
        return -(x + 2 * y - y**2)

    def gradient(self, x, y):
        grad_x = -1
        grad_y = -(2 - 2 * y)
        return grad_x, grad_y

    def hessian(self):
        return [[0, 0],
                [0, 2]]

    def linear_coefs(self):
        return [-1, -2]

    def constraints(self):
        return [
            (3, 2, 6),
            (1, 2, 4),
        ]

Factory.factory_function(Func3())