from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
import numpy as np
from scipy.optimize import minimize

class QuadraticProgramming(BaseAlgorithm):
    name = "quadratic_programming"
    label = "Квадратичное программирование"
    parameters = []

    def optimize(self, function, params):
        c = np.array(function.linear_coefs(), dtype=float)
        D = np.array(function.hessian(), dtype=float)
        raw = function.constraints()
        A = np.array([[r[0], r[1]] for r in raw], dtype=float)
        b = np.array([r[2] for r in raw], dtype=float)

        def objective(x):
            return float(c @ x + 0.5 * (x @ D @ x))

        def gradient(x):
            return c + D @ x

        constraints = [
            {
                "type": "ineq",
                "fun": lambda x, i=i: b[i] - (A[i] @ x)
            }
            for i in range(len(b))
        ]
        bounds = [(0, None), (0, None)]
        x0 = np.array([0.0, 0.0])
        res = minimize(
            objective,
            x0,
            method="SLSQP",
            jac=gradient,
            bounds=bounds,
            constraints=constraints
        )
        x_opt = res.x
        f_opt = function.visualize(float(x_opt[0]), float(x_opt[1]))
        trajectory = [[
            float(x_opt[0]),
            float(x_opt[1]),
            f_opt
        ]]
        if not res.success:
            stop_reason = f"Не сошлось: {res.message}"
            return trajectory, stop_reason
        stop_reason = (
            f"Сошлось: x*=({x_opt[0]:.4f}, {x_opt[1]:.4f}), "
            f"f*={f_opt:.4f}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(QuadraticProgramming())