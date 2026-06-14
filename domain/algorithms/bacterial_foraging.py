from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
from domain.parameter import Parameter
import numpy as np

class BacterialForaging(BaseAlgorithm):
    name = "bfo"
    label = "Бактериальная оптимизация"
    parameters = [
        Parameter(name="n_bacteria", label="Число бактерий (чётное)", type="int", default=20, min=4, max=200, step=2),
        Parameter(name="t_chemo", label="Шаги хемотаксиса", type="int", default=30, min=5, max=200, step=1),
        Parameter(name="t_repro", label="Шаги репродукции", type="int", default=4, min=1, max=20, step=1),
        Parameter(name="t_elim", label="Шаги ликвидации и рассеивания", type="int", default=2, min=1, max=10, step=1),
        Parameter(name="lambda_", label="Величина шага хемотаксиса", type="float", default=0.1, min=0.001, max=2.0, step=0.01),
        Parameter(name="p_elim", label="Вероятность ликвидации", type="float", default=0.25,min=0.0, max=1.0, step=0.01),
        Parameter(name="n_elim", label="Число ликвидируемых бактерий", type="int", default=2, min=1, max=20, step=1),
        Parameter(name="x_min", label="Область поиска (min)", type="float", default=-5.0, min=-100.0, max=0.0, step=0.5),
        Parameter(name="x_max", label="Область поиска (max)", type="float", default=5.0, min=0.0, max=100.0, step=0.5),
    ]

    def optimize(self, function, params):
        n_bact = int(params.get("n_bacteria", 20))
        if n_bact % 2 != 0:
            n_bact += 1
        t_chemo = int(params.get("t_chemo", 30))
        t_repro = int(params.get("t_repro", 4))
        t_elim = int(params.get("t_elim", 2))
        lam = float(params.get("lambda_", 0.1))
        p_elim = float(params.get("p_elim", 0.25))
        n_elim = int(params.get("n_elim", 2))
        lo = float(params.get("x_min", -5.0))
        hi = float(params.get("x_max", 5.0))

        def fitness(pos):
            return function.evaluate(pos[0], pos[1])

        positions = np.random.uniform(lo, hi, (n_bact, 2))

        directions = np.random.uniform(-1, 1, (n_bact, 2))
        norms = np.linalg.norm(directions, axis=1, keepdims=True)
        directions /= (norms + 1e-10)

        trajectory = []
        total_iter = t_elim * t_repro * t_chemo
        log_every  = max(1, total_iter // 100)
        iter_count = 0

        for l in range(t_elim):
            for r in range(t_repro):
                health = np.zeros(n_bact)

                for t in range(t_chemo):
                    for i in range(n_bact):

                        phi_current = fitness(positions[i])
                        new_pos = positions[i] + lam * directions[i]
                        new_pos = np.clip(new_pos, lo, hi)
                        phi_new = fitness(new_pos)

                        if phi_new > phi_current:
                            positions[i] = new_pos
                            health[i] += phi_new
                        else:
                            v = np.random.uniform(-1, 1, 2)
                            directions[i] = v / (np.linalg.norm(v) + 1e-10)
                            health[i] += phi_current

                    best_idx = np.argmax([fitness(p) for p in positions])
                    best_pos = positions[best_idx]
                    if iter_count % log_every == 0:
                        trajectory.append([
                            float(best_pos[0]),
                            float(best_pos[1]),
                            float(function.visualize(best_pos[0], best_pos[1]))
                        ])
                    iter_count += 1

                sorted_idx = np.argsort(health)[::-1]
                positions = positions[sorted_idx]
                directions = directions[sorted_idx]

                half = n_bact // 2
                positions = np.vstack([positions[:half], positions[:half]])

                dirs_clone = np.random.uniform(-1, 1, (half, 2))
                dirs_clone /= np.linalg.norm(dirs_clone, axis=1, keepdims=True) + 1e-10
                directions = np.vstack([directions[:half], dirs_clone])

            for _ in range(n_elim):
                i_j = np.random.randint(0, n_bact)
                u_j = np.random.uniform(0, 1)
                if u_j > p_elim:
                    positions[i_j] = np.random.uniform(lo, hi, 2)
                    directions[i_j] = np.random.uniform(-1, 1, 2)
                    directions[i_j] /= np.linalg.norm(directions[i_j]) + 1e-10

        fitnesses = [fitness(p) for p in positions]
        best_idx = np.argmax(fitnesses)
        best = positions[best_idx]
        f_opt = function.visualize(float(best[0]), float(best[1]))
        trajectory.append([float(best[0]), float(best[1]), f_opt])
        stop_reason = (
            f"Сошлось: x*=({best[0]:.4f}, {best[1]:.4f}), "
            f"f*={f_opt:.4f}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(BacterialForaging())