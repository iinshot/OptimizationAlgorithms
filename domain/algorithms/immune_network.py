from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
from domain.parameter import Parameter
import numpy as np

class ImmuneNetwork(BaseAlgorithm):
    name = "immune_network"
    label = "Искусственная иммунная сеть"
    parameters = [
        Parameter(name="pop_size", label="Размер популяции антител", type="int", default=50, min=10, max=500, step=5),
        Parameter(name="n_b", label="Лучшие антитела для клонирования", type="int", default=10, min=1, max=100, step=1),
        Parameter(name="n_c", label="Клоны на антитело", type="int", default=10, min=1, max=100, step=1),
        Parameter(name="n_d", label="Лучшие клоны после мутации", type="int", default=5, min=1, max=50, step=1),
        Parameter(name="alpha", label="Коэффициент мутации", type="float", default=0.5, min=0.01, max=5.0, step=0.01),
        Parameter(name="max_iter", label="Макс. итераций", type="int", default=200, min=10, max=2000, step=10),
        Parameter(name="x_min", label="Область поиска (min)", type="float", default=-5.0,min=-100.,max=0.0, step=0.5),
        Parameter(name="x_max", label="Область поиска (max)", type="float", default=5.0, min=0.0,  max=100, step=0.5),
    ]

    def optimize(self, function, params):
        pop_size = int(params.get("pop_size", 50))
        n_b = int(params.get("n_b", 10))
        n_c = int(params.get("n_c", 10))
        n_d = int(params.get("n_d", 5))
        alpha = float(params.get("alpha", 0.5))
        max_iter = int(params.get("max_iter", 200))
        lo = float(params.get("x_min", -5.0))
        hi = float(params.get("x_max", 5.0))

        def affinity(x):
            return -function.evaluate(x[0], x[1])

        S_b = np.random.uniform(lo, hi, (pop_size, 2))
        trajectory = []
        log_every = max(1, max_iter // 100)

        for iteration in range(max_iter):
            affinities = np.array([affinity(x) for x in S_b])
            best_idx = np.argsort(affinities)[::-1][:n_b]
            best_antibodies = S_b[best_idx]

            S_m = np.repeat(best_antibodies, n_c, axis=0)

            mutation  = alpha * np.random.uniform(-0.5, 0.5, S_m.shape)
            S_m = S_m + mutation
            S_m = np.clip(S_m, lo, hi)

            S_m_affinities = np.array([affinity(x) for x in S_m])
            top_d_idx = np.argsort(S_m_affinities)[::-1][:n_d]
            S_m_best = S_m[top_d_idx]

            S_combined = np.vstack([S_b, S_m_best])
            comb_aff = np.array([affinity(x) for x in S_combined])
            top_idx = np.argsort(comb_aff)[::-1][:pop_size]
            S_b = S_combined[top_idx]

            best = S_b[0]
            if iteration % log_every == 0 or iteration == max_iter - 1:
                trajectory.append([
                    float(best[0]),
                    float(best[1]),
                    float(function.visualize(best[0], best[1]))
                ])

        best = S_b[0]
        f_opt = function.visualize(float(best[0]), float(best[1]))
        stop_reason = (
            f"Сошлось: x*=({best[0]:.4f}, {best[1]:.4f}), "
            f"f*={f_opt:.4f}, итераций: {max_iter}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(ImmuneNetwork())