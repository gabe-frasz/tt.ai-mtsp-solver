import random


class GeneticAlgorithm:
    def __init__(
        self,
        population_size: int,
        generations: int,
        mutation_rate: float,
        crossover_rate: float,
        elitism_count: int = 1,
    ):
        self.population_size = population_size
        self.generations = generations
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_count = elitism_count

    def run(self, problem):
        population = problem.initialize(self.population_size)
        generation_history = []

        best_overall_individual = None
        best_overall_fitness = float("-inf")

        for gen in range(self.generations):
            evaluated_population = []
            for individual in population:
                fitness = problem.fitness(individual)
                evaluated_population.append((individual, fitness))

            evaluated_population.sort(key=lambda x: x[1], reverse=True)

            curr_best_individual, curr_best_fitness = evaluated_population[0]
            _, curr_worst_fitness = evaluated_population[-1]

            if curr_best_fitness > best_overall_fitness:
                best_overall_fitness = curr_best_fitness
                best_overall_individual = curr_best_individual

            if gen % 10 == 0 or gen == self.generations - 1:
                generation_history.append((gen, curr_best_fitness, curr_worst_fitness))

            new_population = [
                evaluated_population[i][0] for i in range(self.elitism_count)
            ]

            while len(new_population) < self.population_size:
                parent1 = self._tournament_selection(evaluated_population)
                parent2 = self._tournament_selection(evaluated_population)

                if random.random() < self.crossover_rate:
                    offspring1, offspring2 = problem.crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random.random() < self.mutation_rate:
                    offspring1 = problem.mutate(offspring1)
                    offspring2 = problem.mutate(offspring2)

                new_population.extend([offspring1, offspring2])

            population = new_population[: self.population_size]

        return best_overall_individual, best_overall_fitness, generation_history

    def _tournament_selection(
        self, evaluated_population: list[tuple[list[int], float]], k: int = 3
    ):
        tournament_group = random.sample(evaluated_population, k)
        tournament_group.sort(key=lambda x: x[1], reverse=True)
        return tournament_group[0][0]
