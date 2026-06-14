from domain.abstractions.algorithm import BaseAlgorithm
from domain.factory import Factory
from domain.parameter import Parameter
import numpy as np

class GeneticAlgorithm(BaseAlgorithm):
    name = "genetic_algorithm"
    label = "Генетический"
    parameters = [
        Parameter(name="pop_size", label="Размер популяции", type="int", default=100, min=10,  max=500, step=10),
        Parameter(name="generations", label="Поколений", type="int", default=200, min=10, max=1000, step=10),
        Parameter(name="mutation", label="Вероятность мутации", type="float", default=0.1, min=0.01, max=1.0, step=0.01),
        Parameter(name="elite_frac", label="Доля элиты", type="float", default=0.1, min=0.0, max=0.5, step=0.01),
    ]

    def optimize(self, function, params):
        pop_size = int(params.get("pop_size", 100))
        generations = int(params.get("generations", 200))
        mutation = float(params.get("mutation", 0.1))
        elite_n = max(1, int(pop_size * 0.1))
        pop = np.random.uniform(-2, 2, (pop_size, 2))
        trajectory = []

        for gen in range(generations):
            fitness = np.array([function.evaluate(p[0], p[1]) for p in pop])
            best_idx = np.argmin(fitness)
            best = pop[best_idx]
            trajectory.append([
                float(best[0]), float(best[1]),
                float(function.visualize(best[0], best[1]))
            ])
            sorted_idx = np.argsort(fitness)
            elites = pop[sorted_idx[:elite_n]]

            def tournament(k=3):
                idx = np.random.choice(pop_size, k, replace=False)
                return pop[idx[np.argmin(fitness[idx])]].copy()

            children = []
            while len(children) < pop_size - elite_n:
                parent1 = tournament()
                parent2 = tournament()
                alpha = np.random.uniform(0, 1, 2)
                child = alpha * parent1 + (1 - alpha) * parent2
                child += np.random.normal(0, mutation, 2)
                children.append(child)

            pop = np.vstack([elites, np.array(children)])

        fitness = np.array([function.evaluate(p[0], p[1]) for p in pop])
        best = pop[np.argmin(fitness)]
        f_opt = function.visualize(float(best[0]), float(best[1]))

        stop_reason = (
            f"Сошлось: x*=({best[0]:.4f}, {best[1]:.4f}), "
            f"f*={f_opt:.4f}, поколений: {generations}"
        )
        return trajectory, stop_reason

Factory.factory_algorithm(GeneticAlgorithm())