import random

from core.base_problem import BaseProblem
from core.utils import Utils


class MTSP(BaseProblem):
    def __init__(
        self,
        cities: list[list[int, int]],
        depot: list[int, int],
        num_workers: int,
        min_cities_per_worker: int,
        max_cities_per_worker: int,
        max_difference_per_worker: int,
        max_distance_per_worker: float,
        v: float,
        alpha: float,
        beta: float,
        penalty_multiplier: float,
        **kwargs
    ):
        # Map cities to a numbered dict
        self.cities = {i: tuple(coord) for i, coord in enumerate(cities, start=1)}
        self.depot = tuple(depot)
        self.num_workers = num_workers

        # Hyperparameters and constraints
        self.min_cities_per_worker = min_cities_per_worker
        self.max_cities_per_worker = max_cities_per_worker
        self.max_difference_per_worker = max_difference_per_worker
        self.max_distance_per_worker = max_distance_per_worker
        self.v = v
        self.alpha = alpha
        self.beta = beta
        self.penalty_multiplier = penalty_multiplier

        # We need num_workers - 1 dummy nodes to divide workers trajectories in the same list
        num_cities = len(cities)
        num_dummy_nodes = num_workers - 1

        # Genes available for mutation and crossover
        self.valid_genes = list(range(1, num_cities + 1)) + list(
            range(num_cities + 1, num_cities + 1 + num_dummy_nodes)
        )

        # Pre-calculate distance matrix to save cpu cycles
        self.distance_matrix = self._build_distance_matrix()

    def initialize(self, population_size: int):
        population = []
        greedy_count = max(1, population_size // 20)

        for i in range(population_size):
            if i < greedy_count:
                chromosome = self._generate_greedy_chromosome()
            else:
                chromosome = self.valid_genes.copy()
                random.shuffle(chromosome)
            population.append(chromosome)
        return population

    def fitness(self, chromosome: list[int]):
        routes = self._decode_chromosome(chromosome)
        route_distances = []
        route_lengths = []
        total_distance = 0.0
        
        for route in routes:
            route_len = len(route)
            route_lengths.append(route_len)
            if route_len == 0:
                route_distances.append(0.0)
                continue
            curr_route_distance = self.distance_matrix[0][route[0]]
            for i in range(route_len - 1):
                curr_route_distance += self.distance_matrix[route[i]][route[i+1]]
            curr_route_distance += self.distance_matrix[route[-1]][0]
            route_distances.append(curr_route_distance)
            total_distance += curr_route_distance
            
        std_dev = Utils.calc_std_dev(route_distances)
        min_cities_violations = 0
        max_cities_violations = 0
        max_distance_violations = 0.0
        
        for i in range(self.num_workers):
            if route_lengths[i] < self.min_cities_per_worker:
                min_cities_violations += (self.min_cities_per_worker - route_lengths[i])
            if route_lengths[i] > self.max_cities_per_worker:
                max_cities_violations += (route_lengths[i] - self.max_cities_per_worker)
            if route_distances[i] > self.max_distance_per_worker:
                max_distance_violations += (route_distances[i] - self.max_distance_per_worker)
                
        length_diff = max(route_lengths) - min(route_lengths)
        balance_violations = max(0, length_diff - self.max_difference_per_worker)
        
        total_penalties = (min_cities_violations * self.penalty_multiplier) + \
                          (max_cities_violations * self.penalty_multiplier) + \
                          (balance_violations * self.penalty_multiplier) + \
                          (max_distance_violations * self.penalty_multiplier)

        return self.v - total_penalties - (self.alpha * total_distance) - (self.beta * std_dev)

    def crossover(self, parent1: list[int], parent2: list[int]):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))

        def make_offspring(p1, p2):
            offspring = [-1] * size
            offspring[start:end] = p1[start:end]
            p2_ordered = p2[end:] + p2[:end]
            swath_set = set(p1[start:end])
            filtered_p2 = [gene for gene in p2_ordered if gene not in swath_set]
            fill_pos = end
            for gene in filtered_p2:
                offspring[fill_pos % size] = gene
                fill_pos += 1
            return offspring

        return make_offspring(parent1, parent2), make_offspring(parent2, parent1)

    def mutate(self, chromosome: list[int]):
        size = len(chromosome)
        idx1, idx2 = random.sample(range(size), 2)
        if random.random() < 0.8:
            gene = chromosome.pop(idx1)
            chromosome.insert(idx2, gene)
        else:
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

    def format_solution(self, individual: list[int]) -> dict:
        routes = self._decode_chromosome(individual)
        parsed_data = []
        route_distances = []
        total_distance = 0.0

        for i, route in enumerate(routes):
            full_route = [0] + route + [0]
            route_len = len(full_route)
            curr_route_distance = 0.0
            cities_coords = []
            for j in range(route_len - 1):
                curr_route_distance += self.distance_matrix[full_route[j]][full_route[j+1]]
                node = full_route[j]
                cities_coords.append(self.cities[node] if node != 0 else self.depot)
            cities_coords.append(self.depot)
            parsed_data.append({"route": cities_coords, "distance": curr_route_distance})
            route_distances.append(curr_route_distance)
            total_distance += curr_route_distance

        std_dev = Utils.calc_std_dev(route_distances)
        violations = self._get_violations_report(individual)
        fitness = self.fitness(individual)
        is_valid = violations == "0"

        report = []
        report.append("\n" + "="*40)
        report.append("MTSP SOLUTION REPORT")
        report.append("="*40)
        for i, data in enumerate(parsed_data):
            report.append(f"\nWorker {i + 1}:")
            report.append(f"  Distance: {data['distance']:.2f}")
            report.append(f"  Path: {' -> '.join(map(str, data['route']))}")
        report.append("\n" + "-"*40)
        report.append(f"Total Distance: {total_distance:.2f}")
        report.append(f"Standard Deviation: {std_dev:.2f}")
        report.append(f"Fitness Score: {fitness:.2f}")
        report.append(f"Violations: {violations}")
        report.append(f"Status: {'VALID' if is_valid else 'INVALID'}")
        report.append("-"*40 + "\n")

        return {
            "raw_chromosome": individual,
            "fitness_score": fitness,
            "is_valid": is_valid,
            "domain_metrics": {
                "total_distance": total_distance,
                "std_dev": std_dev,
                "route_distances": route_distances,
                "violations": violations
            },
            "parsed_data": parsed_data,
            "human_report": "\n".join(report)
        }

    def _get_violations_report(self, chromosome: list[int]):
        routes = self._decode_chromosome(chromosome)
        route_distances = []
        route_lengths = []
        for route in routes:
            route_len = len(route)
            route_lengths.append(route_len)
            if route_len == 0:
                route_distances.append(0.0)
                continue
            d = self.distance_matrix[0][route[0]]
            for i in range(route_len - 1):
                d += self.distance_matrix[route[i]][route[i+1]]
            d += self.distance_matrix[route[-1]][0]
            route_distances.append(d)

        min_cities_v = 0
        max_cities_v = 0
        max_dist_v_count = 0
        for i in range(self.num_workers):
            if route_lengths[i] < self.min_cities_per_worker:
                min_cities_v += (self.min_cities_per_worker - route_lengths[i])
            if route_lengths[i] > self.max_cities_per_worker:
                max_cities_v += (route_lengths[i] - self.max_cities_per_worker)
            if route_distances[i] > self.max_distance_per_worker:
                max_dist_v_count += 1
        diff = max(route_lengths) - min(route_lengths)
        balance_v = max(0, diff - self.max_difference_per_worker)
        v_list = []
        if min_cities_v > 0: v_list.append(f"{min_cities_v} (R4)")
        if max_cities_v > 0: v_list.append(f"{max_cities_v} (R5)")
        if balance_v > 0: v_list.append(f"{balance_v} (R6)")
        if max_dist_v_count > 0: v_list.append(f"{max_dist_v_count} (R7)")
        return ", ".join(v_list) if v_list else "0"

    def _build_distance_matrix(self):
        matrix_size = len(self.cities) + 1
        distance_matrix = [[0.0] * matrix_size for _ in range(matrix_size)]
        all_nodes = {0: self.depot}
        all_nodes.update(self.cities)
        for i in range(matrix_size):
            for j in range(i + 1, matrix_size):
                distance_matrix[i][j] = Utils.calc_euclidean_distance(all_nodes[i], all_nodes[j])
                distance_matrix[j][i] = distance_matrix[i][j]
        return distance_matrix

    def _generate_greedy_chromosome(self):
        chromosome = []
        unvisited = list(range(1, len(self.cities) + 1))
        target_cities = len(self.cities) // self.num_workers
        dummy_node = len(self.cities) + 1
        for worker in range(self.num_workers):
            if not unvisited: break
            first_city = random.choice(unvisited)
            chromosome.append(first_city)
            unvisited.remove(first_city)
            current_node = first_city
            cities_assigned = 1
            while unvisited and cities_assigned < target_cities:
                nearest_city = min(unvisited, key=lambda c: self.distance_matrix[current_node][c])
                chromosome.append(nearest_city)
                unvisited.remove(nearest_city)
                current_node = nearest_city
                cities_assigned += 1
            if worker < self.num_workers - 1:
                chromosome.append(dummy_node)
                dummy_node += 1
        if unvisited:
            chromosome.extend(unvisited)
        return chromosome

    def _decode_chromosome(self, chromosome: list[int]):
        routes = [[] for _ in range(self.num_workers)]
        curr_worker = 0
        cities_count = len(self.cities)
        for gene in chromosome:
            if gene <= cities_count:
                routes[curr_worker].append(gene)
            else:
                curr_worker += 1
        return routes
