from domain.factory import Factory
import numpy as np

class OptimizationService:
    def run(self, algo_name, func_name, params):
        algo = Factory.algorithms[algo_name]
        func = Factory.functions[func_name]
        trajectory, stop_reason = algo.optimize(func, params)
        surface = self._build_surface(func)

        last = trajectory[-1]
        return {
            "trajectory": trajectory,
            "surface": surface,
            "info": {
                "steps": len(trajectory),
                "min_point": [last[0], last[1]],
                "min_value": last[2],
                "stop_reason": stop_reason
            }
        }

    def _build_surface(self, func):
        if hasattr(func, 'plot_bounds'):
            lo, hi = func.plot_bounds()
        else:
            lo, hi = -5, 5

        x_vals = [round(x, 2) for x in np.linspace(lo, hi, 60)]
        y_vals = [round(y, 2) for y in np.linspace(lo, hi, 60)]

        z_grid = []
        for y in y_vals:
            row = []
            for x in x_vals:
                row.append(func.visualize(x, y))
            z_grid.append(row)

        return {"z": z_grid, "x": x_vals, "y": y_vals}