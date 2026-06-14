from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
from domain.parameter import Parameter
import numpy as np

class BeeAlgorithm(BaseAlgorithm):
    name = "bee_algorithm"
    label = "Пчелиный алгоритм (B-алгоритм)"
    parameters = [
        Parameter(name="scouts", label="Пчёлы-разведчики", type="int", default=16, min=4, max=100, step=1),
        Parameter(name="elite_sites", label="Элитные участки", type="int", default=2, min=1, max=10, step=1),
        Parameter(name="best_sites", label="Перспективные участки",type="int", default=3, min=1, max=10, step=1),
        Parameter(name="elite_bees", label="Пчёлы на элитном участке", type="int", default=7, min=1, max=50, step=1),
        Parameter(name="best_bees", label="Пчёлы на персп. участке",type="int", default=4, min=1, max=50, step=1),
        Parameter(name="radius", label="Радиус участков", type="float", default=0.2, min=0.01, max=5.0, step=0.01),
        Parameter(name="max_iter", label="Макс. итераций", type="int", default=500, min=10, max=2000, step=10),
        Parameter(name="stagnation", label="Стагнация итераций", type="int", default=20, min=5, max=100, step=1),
        Parameter(name="x_min", label="Область поиска (min)", type="float", default=-5.0, min=-100., max=0.0, step=0.5),
        Parameter(name="x_max", label="Область поиска (max)", type="float", default=5.0, min=0.0, max=100., step=0.5),
    ]

    def optimize(self, function, params):
        n_scouts = int(params.get("scouts", 16))
        n_elite_sites = int(params.get("elite_sites", 2))
        n_best_sites = int(params.get("best_sites", 3))
        n_elite_bees = int(params.get("elite_bees", 7))
        n_best_bees = int(params.get("best_bees", 4))
        radius = float(params.get("radius", 0.2))
        max_iter = int(params.get("max_iter", 500))
        stagnation = int(params.get("stagnation", 20))
        lo = float(params.get("x_min", -5.0))
        hi = float(params.get("x_max", 5.0))

        def fitness(x, y):
            return -function.evaluate(x, y)

        def send_scouts():
            pts = np.random.uniform(lo, hi, (n_scouts, 2))
            scored = [(fitness(p[0], p[1]), p) for p in pts]
            scored.sort(key=lambda t: t[0], reverse=True)
            return scored

        def local_search(center, n_bees, r):
            best_fit = fitness(center[0], center[1])
            best_pos = center.copy()
            for _ in range(n_bees):
                candidate = center + np.random.uniform(-r, r, 2)
                candidate = np.clip(candidate, lo, hi)
                f = fitness(candidate[0], candidate[1])
                if f > best_fit:
                    best_fit = f
                    best_pos = candidate.copy()
            return best_fit, best_pos

        def filter_overlapping(centers, radius, eps=None):
            if eps is None:
                eps = radius * 2
            filtered = []
            for c in centers:
                too_close = any(np.linalg.norm(c - f) < eps for f in filtered)
                if not too_close:
                    filtered.append(c)
            return filtered

        trajectory = []
        log_every = max(1, max_iter // 100)
        scored = send_scouts()
        global_best_fit = scored[0][0]
        global_best_pos = scored[0][1].copy()
        stag_count = 0

        for iteration in range(max_iter):
            elite_centers = filter_overlapping([s[1] for s in scored[:n_elite_sites]], radius)
            best_centers = filter_overlapping([s[1] for s in scored[n_elite_sites:n_elite_sites + n_best_sites]], radius)
            new_points = []

            for center in elite_centers:
                f, pos = local_search(center, n_elite_bees, radius)
                new_points.append((f, pos))

            for center in best_centers:
                f, pos = local_search(center, n_best_bees, radius)
                new_points.append((f, pos))

            n_remaining = n_scouts - len(new_points)
            for _ in range(n_remaining):
                pt = np.random.uniform(lo, hi, 2)
                f = fitness(pt[0], pt[1])
                new_points.append((f, pt))

            scored = sorted(new_points, key=lambda t: t[0], reverse=True)

            if scored[0][0] > global_best_fit:
                global_best_fit = scored[0][0]
                global_best_pos = scored[0][1].copy()
                stag_count = 0
            else:
                stag_count += 1

            if iteration % log_every == 0 or iteration == max_iter - 1:
                trajectory.append([
                    float(global_best_pos[0]),
                    float(global_best_pos[1]),
                    float(function.visualize(global_best_pos[0], global_best_pos[1]))
                ])

            if stag_count >= stagnation:
                break

        f_opt = function.visualize(float(global_best_pos[0]), float(global_best_pos[1]))
        stop_reason = (
            f"Сошлось: x*=({global_best_pos[0]:.4f}, {global_best_pos[1]:.4f}), "
            f"f*={f_opt:.4f}, итераций: {iteration + 1}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(BeeAlgorithm())