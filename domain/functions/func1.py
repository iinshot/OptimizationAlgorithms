from domain.abstractions.function import BaseFunction
from domain.factory import Factory

class Func1(BaseFunction):
    name = "func1"
    label = "2 * x^2 + x * y + y^2"
    parameters = []

    def evaluate(self, x, y):
        return 2 * x ** 2 + x * y + y ** 2

    def gradient(self, x, y):
        grad_x = 4 * x + y
        grad_y = x + 2 * y
        return grad_x, grad_y

Factory.factory_function(Func1())