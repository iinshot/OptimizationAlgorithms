from domain.abstractions.algorithm import BaseAlgorithm
from domain.parameter import Parameter
from domain.factory import Factory
import math

class GradientDescent(BaseAlgorithm):
    name = "gradient_descent"
    label = "Градиентный спуск (постоянный шаг)"
    parameters = [
        Parameter(name="lr", label="Шаг обучения (постоянный)", type="float", default=0.1, min=0.001, max=1.0, step=0.01),
        Parameter(name="epsilon1", label="ε₁ (норма градиента)", type="float", default=0.1, min=1e-6, max=1.0, step=0.01),
        Parameter(name="epsilon2", label="ε₂ (разность точек/значений)", type="float", default=0.15, min=1e-6, max=1.0, step=0.01),
        Parameter(name="max_iter", label="M (макс. итераций)", type="int", default=10, min=1, max=100),
        Parameter(name="x0", label="Начальная x₁", type="float", default=0.5),
        Parameter(name="y0", label="Начальная x₂", type="float", default=1.0)
    ]

    def optimize(self, function, params):
        lr = params["lr"]
        eps1 = params["epsilon1"]
        eps2 = params["epsilon2"]
        max_iter = params["max_iter"]
        x = params["x0"]
        y = params["y0"]

        trajectory = []
        k = 0
        prev_x, prev_y = None, None
        prev_value = None
        double_stop_count = 0
        stop_reason = "Неизвестно"

        while k < max_iter:
            value = function.evaluate(x, y)
            trajectory.append([x, y, value])

            grad_x, grad_y = function.gradient(x, y)
            grad_norm = math.hypot(grad_x, grad_y)

            if grad_norm < eps1:
                stop_reason = f"Норма град: {grad_norm:.2e} < ε₁={eps1:.2e}"
                break

            new_x = x - lr * grad_x
            new_y = y - lr * grad_y
            new_value = function.evaluate(new_x, new_y)

            if prev_x is not None:
                delta_x = math.hypot(new_x - prev_x, new_y - prev_y)
                delta_f = abs(new_value - prev_value)

                if delta_x < eps2 and delta_f < eps2:
                    double_stop_count += 1
                    if double_stop_count >= 2:
                        stop_reason = f"|Δx|={delta_x:.3f} < ε₂ и |Δf|={delta_f:.3f} < ε₂"
                        break
                else:
                    double_stop_count = 0

            prev_x, prev_y = x, y
            prev_value = value
            x, y = new_x, new_y
            k += 1

        if k >= max_iter:
            stop_reason = f"Достигнут лимит итераций M={max_iter}"

        return trajectory, stop_reason

Factory.factory_algorithm(GradientDescent())