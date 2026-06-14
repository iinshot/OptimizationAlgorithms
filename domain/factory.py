class Factory:
    algorithms = {}
    functions = {}

    @classmethod
    def factory_algorithm(cls, algo):
        cls.algorithms[algo.name] = algo

    @classmethod
    def factory_function(cls, func):
        cls.functions[func.name] = func