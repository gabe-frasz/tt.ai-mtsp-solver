import random

from src.utils import Utils

# Constraints
MIN_CITIES_PER_WORKER = 5
MAX_CITIES_PER_WORKER = 15
MAX_DIFFERENCE_PER_WORKER = 5
MAX_DISTANCE_PER_WORKER = 350.0

# Objective-Scaled weights and base formula constants
V = 10000.0
ALPHA = 1.0 # weight for total distance
BETA = 3.0  # weight for standard deviation (forces balanced distances)
PENALTY_MULTIPLIER = V * 0.5

class MTSP:
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
        # Excluding depot (0) since it MUST be at the start and end of all individuals
        self.valid_genes = list(range(1, num_cities + 1)) + list(
            range(num_cities + 1, num_cities + 1 + num_dummy_nodes)
        )

        # Pre-calculate distance matrix to save cpu cycles (O(1) lookups)
        self.distance_matrix = self._build_distance_matrix()

    def initialize(self, population_size: int):
        """
        Generates the population with majority of random chromosomes and a few greedy ones.
        """
        population = []
        greedy_count = max(1, population_size // 20) # 5% of the population

        for i in range(population_size):
            if i < greedy_count:
                chromosome = self._generate_greedy_chromosome()
            else:
                chromosome = self.valid_genes.copy()
                random.shuffle(chromosome)

            population.append(chromosome)

        return population

    def fitness(self, chromosome: list[int]):
        """
        Calculates total distance, standard deviation, 
        and applies Objective-Scaled Penalties for constraints R4 to R7.
        Higher fitness score is better.
        """
        routes = self._decode_chromosome(chromosome)
        
        route_distances = []
        route_lengths = []
        total_distance = 0.0
        
        # 1. Calculate route distances
        for route in routes:
            route_len = len(route)
            route_lengths.append(route_len)
            
            if route_len == 0:
                route_distances.append(0.0)
                continue
                
            # Distance from depot (0) to the first city
            curr_route_distance = self.distance_matrix[0][route[0]]
            
            # Distance between consecutive cities
            for i in range(route_len - 1):
                curr_route_distance += self.distance_matrix[route[i]][route[i+1]]
                
            # Distance from the last city back to depot (0)
            curr_route_distance += self.distance_matrix[route[-1]][0]
            
            route_distances.append(curr_route_distance)
            total_distance += curr_route_distance
            
        # 2. Calculate standard deviation
        std_dev = Utils.calc_std_dev(route_distances)
        
        # 3. Calculate constraint violations
        min_cities_violations = 0
        max_cities_violations = 0
        max_distance_violations = 0.0
        
        for i in range(self.num_workers):
            if route_lengths[i] < MIN_CITIES_PER_WORKER:
                min_cities_violations += (MIN_CITIES_PER_WORKER - route_lengths[i])
                
            if route_lengths[i] > MAX_CITIES_PER_WORKER:
                max_cities_violations += (route_lengths[i] - MAX_CITIES_PER_WORKER)
                
            if route_distances[i] > MAX_DISTANCE_PER_WORKER:
                max_distance_violations += (route_distances[i] - MAX_DISTANCE_PER_WORKER)
                
        length_diff = max(route_lengths) - min(route_lengths)
        balance_violations = max(0, length_diff - MAX_DIFFERENCE_PER_WORKER)
        
        # Apply Objective-Scaled penalties and return the total score
        total_penalties = (min_cities_violations * PENALTY_MULTIPLIER) + \
                          (max_cities_violations * PENALTY_MULTIPLIER) + \
                          (balance_violations * PENALTY_MULTIPLIER) + \
                          (max_distance_violations * PENALTY_MULTIPLIER)

        return V - total_penalties - (ALPHA * total_distance) - (BETA * std_dev)

    def crossover(self, parent1: list[int], parent2: list[int]):
        """
        Order Crossover (OX) applied to the entire chromosome (cities + dummy nodes).
        Guarantees that no cities or dummy nodes are duplicated or lost.
        """
        size = len(parent1) # every chromosome has the same size
        start, end = sorted(random.sample(range(size), 2)) # swath selection (two cut points)

        def make_offspring(p1, p2):
            offspring = [-1] * size # fill with -1 fallback
            offspring[start:end] = p1[start:end] # copy the exact swath from p1
        
            # Copy p2 starting from 'end' to finish, then append the rest from beginning
            p2_ordered = p2[end:] + p2[:end]
        
            # Keep only the genes that are NOT already in offspring
            swath_set = set(p1[start:end])
            filtered_p2 = [gene for gene in p2_ordered if gene not in swath_set]
        
            # Fill remaining empty spots in offspring starting from 'end'
            fill_pos = end
            for gene in filtered_p2:
                offspring[fill_pos % size] = gene
                fill_pos += 1
            
            return offspring

        return make_offspring(parent1, parent2), make_offspring(parent2, parent1)

    def mutate(self, chromosome: list[int]):
        """
        Applies mutation to the chromosome in-place.
        Weighted choice: 80% Insert (Inter-route Migration) and 20% Swap (Intra-route).
        """
        size = len(chromosome)
        idx1, idx2 = random.sample(range(size), 2)

        if random.random() < 0.8:
            # Insert: moves a city/dummy to a new position
            gene = chromosome.pop(idx1)
            chromosome.insert(idx2, gene)
        else:
            # Swap: just exchanges two positions
            chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]

    def get_solution_from_individual(self, individual: list[int]):
        """
        Translates the individual chromosome into a list of routes.
        Each route is a list of cities + depot (0) and the distance between them.
        Returns a tuple: (solution, violations_report, std_dev)
        """
        routes = self._decode_chromosome(individual)
        solution = []
        route_distances = []

        for i, route in enumerate(routes):
            full_route = [0] + route + [0] # add depot to the beginning and end
            route_len = len(full_route)
            curr_route_distance = 0.0
            cities_coords = []

            # Distance between consecutive cities (including depot)
            for j in range(route_len - 1):
                curr_route_distance += self.distance_matrix[full_route[j]][full_route[j+1]]
                
                # Also get the coordinates of the cities
                node = full_route[j]
                cities_coords.append(self.cities[node] if node != 0 else self.depot)
                
            # Add the last depot coord
            cities_coords.append(self.depot)

            solution.append((cities_coords, curr_route_distance))
            route_distances.append(curr_route_distance)

        # Calculate standard deviation
        std_dev = Utils.calc_std_dev(route_distances)

        return solution, self._get_violations_report(individual), std_dev

    def _get_violations_report(self, chromosome: list[int]):
        """
        Groups violations in a single string like "2 (R4), 0 (R5), 50 (R7)".
        Returns "0" if there are no violations.
        """
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
            if route_lengths[i] < MIN_CITIES_PER_WORKER:
                min_cities_v += (MIN_CITIES_PER_WORKER - route_lengths[i])
            if route_lengths[i] > MAX_CITIES_PER_WORKER:
                max_cities_v += (route_lengths[i] - MAX_CITIES_PER_WORKER)
            if route_distances[i] > MAX_DISTANCE_PER_WORKER:
                max_dist_v_count += 1
        
        diff = max(route_lengths) - min(route_lengths)
        balance_v = max(0, diff - MAX_DIFFERENCE_PER_WORKER)

        v_list = []
        if min_cities_v > 0: v_list.append(f"{min_cities_v} (R4)")
        if max_cities_v > 0: v_list.append(f"{max_cities_v} (R5)")
        if balance_v > 0: v_list.append(f"{balance_v} (R6)")
        if max_dist_v_count > 0: v_list.append(f"{max_dist_v_count} (R7)")

        return ", ".join(v_list) if v_list else "0"


    def _build_distance_matrix(self):
        """
        Calculates the distance between all cities and the depot (0th index).
        Returns a square matrix of size (num_cities + 1).
        """
        matrix_size = len(self.cities) + 1 # +1 for depot
        distance_matrix = [[0.0] * matrix_size for _ in range(matrix_size)] # fill with 0.0 fallback

        # Merge cities and depot (0) into one dict
        all_nodes = {0: self.depot}
        all_nodes.update(self.cities)

        # Since the matrix is symmetric, just calculate the upper triangle
        # Also skip diagonal because when i == j, cities are the same, so distance is 0.0
        for i in range(matrix_size):
            for j in range(i + 1, matrix_size):
                distance_matrix[i][j] = Utils.calc_euclidean_distance(all_nodes[i], all_nodes[j])
                distance_matrix[j][i] = distance_matrix[i][j]

        return distance_matrix

    def _generate_greedy_chromosome(self):
        """
        Generates a chromosome using the Nearest Neighbor Strategy.
        Guarantees perfect balance of cities.
        """
        chromosome = []
        unvisited = list(range(1, len(self.cities) + 1))
        target_cities = len(self.cities) // self.num_workers # divide cities evenly
        
        dummy_node = len(self.cities) + 1 # first dummy node ID
        
        for worker in range(self.num_workers):
            if not unvisited: break
            
            # 1. Select the first city to create diversity in the elite
            first_city = random.choice(unvisited)
            chromosome.append(first_city)
            unvisited.remove(first_city)
            
            current_node = first_city
            cities_assigned = 1
            
            # 2. Fill the rest of the chromosome with the nearest cities
            while unvisited and cities_assigned < target_cities:
                # Find the minimum value based on distance
                nearest_city = min(unvisited, key=lambda c: self.distance_matrix[current_node][c])
                
                chromosome.append(nearest_city)
                unvisited.remove(nearest_city)
                current_node = nearest_city
                cities_assigned += 1
                
            # 3. Insert dummy node if it's not the last worker
            if worker < self.num_workers - 1:
                chromosome.append(dummy_node)
                dummy_node += 1
                
        # If there's any leftover cities, add them to the end
        if unvisited:
            chromosome.extend(unvisited)
            
        return chromosome

    def _decode_chromosome(self, chromosome: list[int]):
        """
        Translates the 1D chromosome array into specific routes for each worker.
        Splits the array whenever a dummy node (ID > len(cities)) is found.
        """
        routes = [[] for _ in range(self.num_workers)]
        curr_worker = 0
        cities_count = len(self.cities)

        for gene in chromosome:
            if gene <= cities_count:
                # It's a real city, add to current worker's route
                routes[curr_worker].append(gene)
            else:
                # It's a dummy node (delimiter), update current worker
                curr_worker += 1
                
        return routes


class MTSPLogger:
    def __init__(self, total_generations: int, step: int = 20):
        self.total = total_generations
        self.step = max(1, total_generations // step)

    def print_header(self):
        print(f"{'Gen':>5} | {'Max Fitness':>12} | {'Avg Fitness':>12} | {'Min Fitness':>12}")
        print("-" * 51)

    def log(self, gen: int, max_fit: float, avg_fit: float, min_fit: float):
        # Print and save progress at a regular interval and at the end
        if gen % self.step == 0 or gen == self.total - 1:
            print(f"{gen:5d} | {max_fit:12.2f} | {avg_fit:12.2f} | {min_fit:12.2f}")
