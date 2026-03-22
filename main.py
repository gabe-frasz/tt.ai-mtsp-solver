from src.genetic_algorithm import GeneticAlgorithm
from src.mtsp import MTSP, MTSPLogger
from src.parser import get_config


def main():
    config = get_config()

    print("🚀 Initilizing MTSP Solver...")
    print(f"⚙️ Final Configuration: Pop: {config['pop_size']} | Gen: {config['generations']} | Mut: {config['mutation_rate']} | Cross: {config['crossover_rate']}")
    print()

    problem = MTSP(CITIES, DEPOT)
    logger = MTSPLogger(total_generations=config["generations"])

    ga = GeneticAlgorithm(
        population_size=config["pop_size"],
        generations=config["generations"],
        crossover_rate=config["crossover_rate"],
        mutation_rate=config["mutation_rate"],
        elitism_count=config["elitism_count"],
        logger=logger,
    )

    solution, violations, std_dev, fitness = ga.run(problem)

    for worker, route in enumerate(solution):
        print(f"\nWorker {worker + 1} - Distance: {route[1]:.2f}:")
        print(*route[0], sep=" → ")

    print(f"\nTotal distance: {sum(route[1] for route in solution):.2f}")
    print(f"Standard Deviation between routes: {std_dev:.2f}")
    print(f"Fitness: {fitness:.2f}")
    print(f"Violations: {violations}\n")


DEPOT = (30, 30)
CITIES = [
    (5, 10),
    (15, 25),
    (30, 5),
    (40, 20),
    (20, 40),
    (35, 35),
    (10, 30),
    (50, 45),
    (45, 10),
    (60, 30),
    (25, 15),
    (55, 20),
    (70, 10),
    (80, 25),
    (65, 40),
    (90, 30),
    (75, 50),
    (85, 15),
    (95, 35),
    (40, 50),
    (10, 5),
    (20, 25),
    (35, 10),
    (50, 15),
    (60, 5),
    (70, 20),
    (30, 50),
    (45, 25),
    (55, 35),
    (65, 15),
]


if __name__ == "__main__":
    main()
