from core.factory import problem_factory
from core.ga import GeneticAlgorithm
from core.logger import GALogger
from core.parser import get_config


def main():
    config = get_config()

    ga_config = config["ga_config"]
    problem_name = config["problem_name"]
    problem_config = config["problem_config"]

    print(f"🚀 Initializing {problem_name.upper()} Solver...")
    print(f"⚙️ GA Configuration: Pop: {ga_config['pop_size']} | Gen: {ga_config['generations']} | Mut: {ga_config['mutation_rate']} | Cross: {ga_config['crossover_rate']}")
    print()

    problem = problem_factory(problem_name, **problem_config)
    logger = GALogger(total_generations=ga_config["generations"])
    ga = GeneticAlgorithm(**ga_config, logger=logger)

    best_individual = ga.run(problem)
    solution = problem.format_solution(best_individual)

    print(solution['human_report'])
    print("Debug - Domain Metrics:")
    for metric, value in solution['domain_metrics'].items():
        print(f"  {metric}: {value}")
    print()


if __name__ == "__main__":
    main()
