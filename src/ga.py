import random


class GeneticAlgorithm:
    def __init__(
        self,
        pop_size: int,
        generations: int,
        mutation_rate: float,
        crossover_rate: float,
        elitism_count: int = 1,
        logger = None,
        **kwargs
    ):
        self.pop_size = pop_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count
        self.logger = logger

    def run(self, problem):
        population = problem.initialize(self.pop_size)

        best_overall_individual = None
        best_overall_fitness = float("-inf")

        if self.logger: self.logger.print_header()

        for gen in range(self.generations):
            # Sort individuals by fitness
            evaluated_population = [(ind, problem.fitness(ind)) for ind in population]
            evaluated_population.sort(key=lambda x: x[1], reverse=True)

            curr_best_individual, curr_best_fitness = evaluated_population[0]
            _, curr_worst_fitness = evaluated_population[-1]
            avg_fitness = sum(fit for _, fit in evaluated_population) / self.pop_size

            if curr_best_fitness > best_overall_fitness:
                best_overall_individual = curr_best_individual.copy()

            if self.logger: self.logger.log(gen, curr_best_fitness, avg_fitness, curr_worst_fitness)

            # Elitism: keep the best individuals in the next generation
            new_population = [
                evaluated_population[i][0] for i in range(self.elitism_count)
            ]

            while len(new_population) < self.pop_size:
                parent1 = self._tournament_selection(evaluated_population)
                parent2 = self._tournament_selection(evaluated_population)

                if random.random() < self.crossover_rate:
                    offspring1, offspring2 = problem.crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1.copy(), parent2.copy()

                if random.random() < self.mutation_rate:
                    problem.mutate(offspring1)
                if random.random() < self.mutation_rate:
                    problem.mutate(offspring2)

                new_population.extend([offspring1, offspring2])

            population = new_population[:self.pop_size]

        return best_overall_individual

    def _tournament_selection(
        self, evaluated_population: list[tuple[list[int], float]], k: int = 3
    ):
        """
        Selects the best individual (highest fitness score)
        from a tournament of k randomly selected individuals.
        """
        tournament_group = random.sample(evaluated_population, k)
        tournament_group.sort(key=lambda x: x[1], reverse=True)
        return tournament_group[0][0]
