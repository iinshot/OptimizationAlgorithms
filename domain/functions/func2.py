from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Func2(BaseFunction):
    name = "Func2"
    label = "2x₁² + 3x₂² + 4x₁x₂ − 6x₁ − 3x₂"
    parameters = []

    def evaluate(self, x, y):
        return 2 * x**2 + 3 * y**2 + 4 * x * y - 6 * x - 3 * y

    def gradient(self, x, y):
        grad_x = 4 * x + 4 * y - 6
        grad_y = 6 * y + 4 * x - 3
        return grad_x, grad_y

    def hessian(self):
        return [[4, 4],
                [4, 6]]

    def linear_coefs(self):
        return [-6, -3]

    def constraints(self):
        return [
            (1, 1, 1),
            (2, 3, 4),
        ]

Factory.factory_function(Func2())