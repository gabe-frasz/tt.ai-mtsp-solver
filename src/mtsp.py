import math
import random


class mTSP:
    def __init__(
        self,
        cities_coords: list[tuple[int, int]],
        depot_coord: tuple[int, int],
        num_workers: int = 3,
    ):
        # Map cities to a numbered dict
        self.cities = {i: coords for i, coords in enumerate(cities_coords, start=1)}

        self.depot = depot_coord
        self.num_workers = num_workers

        # We need num_workers - 1 dummy nodes to divide workers trajectories in the same list
        num_cities = len(cities_coords)
        num_dummy_nodes = num_workers - 1

        # Genes available for mutation and crossover
        # All cities (starting at 1) + dummy nodes
        self.valid_genes = list(range(1, num_cities + 1)) + list(
            range(num_cities + 1, num_cities + 1 + num_dummy_nodes)
        )

        # Pre-calculate distance matrix to save cpu cycles (O(1) lookups)
        self.distance_matrix = self._build_distance_matrix()

    def initialize(self, population_size: int):
        population = []
        for _ in range(population_size):
            individual = self.valid_genes.copy()
            random.shuffle(individual)
            population.append(individual)
        return population

    def fitness(self, chromosome: list[int]):
        pass

    def crossover(self, parent1: list[int], parent2: list[int]):
        pass

    def mutate(self, chromosome: list[int], mutation_rate: float):
        pass

    def _distance(self, node1: tuple[int, int], node2: tuple[int, int]):
        # Euclidean distance
        dx = abs(node1[0] - node2[0])
        dy = abs(node1[1] - node2[1])
        return math.sqrt(dx**2 + dy**2)

    def _build_distance_matrix(self):
        # Init matrix with size of all cities + depot
        matrix_size = len(self.cities) + 1
        distance_matrix = [[0.0] * matrix_size for _ in range(matrix_size)]

        # Merge cities and depot into one dict
        all_nodes = {0: self.depot}
        all_nodes.update(self.cities)

        for i in range(matrix_size):
            for j in range(matrix_size):
                # Skip if distance is already calculated
                if distance_matrix[i][j] != 0.0:
                    continue

                if i == j:
                    # Distance to itself is 0
                    distance_matrix[i][j] = 0.0
                else:
                    # Calculate distance between cities (forward and backward)
                    distance_matrix[i][j] = self._distance(all_nodes[i], all_nodes[j])
                    distance_matrix[j][i] = distance_matrix[i][j]

        return distance_matrix
