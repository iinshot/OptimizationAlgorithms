from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
from domain.parameter import Parameter
import numpy as np

class ParticleSwarm(BaseAlgorithm):
    name = "particle_swarm"
    label = "Алгоритм роя частиц"
    parameters = [
        Parameter(name="n_particles", label="Число частиц", type="int", default=30, min=5, max=200, step=5),
        Parameter(name="iterations", label="Число итераций", type="int", default=100, min=10, max=1000, step=10),
        Parameter(name="w", label="Коэф. скорости", type="float", default=0.1, min=0.01,max=1.0, step=0.01),
        Parameter(name="c1", label="Локальный коэф", type="float", default=2.0, min=0.1, max=4.0, step=0.1),
        Parameter(name="c2", label="Глобальный коэф", type="float", default=5.0, min=0.1, max=6.0, step=0.1),
        Parameter(name="x_min", label="Min область поиска", type="float", default=-5.0,min=-500.0,max=0.0,step=0.5),
        Parameter(name="x_max", label="Max область поиска", type="float", default=5.0, min=0.0, max=500.0,step=0.5),
    ]

    def optimize(self, function, params):
        n = int(params.get("n_particles", 30))
        itr = int(params.get("iterations", 100))
        k = float(params.get("w", 0.1))
        phi_p = float(params.get("c1", 2.0))
        phi_g = float(params.get("c2", 5.0))
        lo = float(params.get("x_min", -5.0))
        hi = float(params.get("x_max",  5.0))

        phi = phi_p + phi_g
        common_ratio = 2.0 * k / abs(2.0 - phi - np.sqrt(max(phi**2 - 4.0 * phi, 1e-10)))
        pos = np.random.uniform(lo, hi, (n, 2))
        vel = np.random.uniform(-(hi - lo), (hi - lo), (n, 2))
        p_best_pos = pos.copy()
        p_best_val = np.array([function.evaluate(p[0], p[1]) for p in pos])
        g_best_idx = np.argmin(p_best_val)
        g_best_pos = p_best_pos[g_best_idx].copy()
        g_best_val = p_best_val[g_best_idx]
        trajectory = []
        log_every  = max(1, itr // 100)

        for i in range(itr):
            rp = np.random.rand(n, 2)
            rg = np.random.rand(n, 2)

            vel = common_ratio * (
                vel
                + phi_p * rp * (p_best_pos - pos)
                + phi_g * rg * (g_best_pos - pos)
            )
            pos = pos + vel
            vals = np.array([function.evaluate(p[0], p[1]) for p in pos])
            improved = vals < p_best_val
            p_best_pos[improved] = pos[improved]
            p_best_val[improved] = vals[improved]
            g_idx = np.argmin(p_best_val)
            if p_best_val[g_idx] < g_best_val:
                g_best_pos = p_best_pos[g_idx].copy()
                g_best_val = p_best_val[g_idx]

            if i % log_every == 0 or i == itr - 1:
                trajectory.append([
                    float(g_best_pos[0]),
                    float(g_best_pos[1]),
                    float(function.visualize(g_best_pos[0], g_best_pos[1]))
                ])

        f_opt = function.visualize(float(g_best_pos[0]), float(g_best_pos[1]))
        stop_reason = (
            f"Сошлось: x*=({g_best_pos[0]:.4f}, {g_best_pos[1]:.4f}), "
            f"f*={f_opt:.4f}, итераций: {itr}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(ParticleSwarm())