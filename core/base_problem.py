from abc import ABC, abstractmethod


class BaseProblem(ABC):
    @abstractmethod
    def initialize(self, pop_size: int) -> list[any]:
        """
        Generates the initial population.
        """
        pass

    @abstractmethod
    def fitness(self, individual: any) -> float:
        """
        Calculates the fitness score of an individual.
        Higher score is better.
        """
        pass

    @abstractmethod
    def crossover(self, parent1: any, parent2: any) -> tuple[any, any]:
        """
        Performs crossover between two parents to produce offspring.
        """
        pass

    @abstractmethod
    def mutate(self, individual: any) -> None:
        """
        Performs mutation on an individual in-place.
        """
        pass

    @abstractmethod
    def format_solution(self, individual: any) -> dict[str, any]:
        """
        Translates the individual into a standardized Solution Envelope.
        
        Returns a dictionary with exactly these keys:
            raw_chromosome (list): The raw output from the GA.
            fitness_score (float): The final score.
            is_valid (bool): True if no hard constraints are violated.
            domain_metrics (dict): Problem-specific numerical metrics.
            parsed_data (any): Structured data representing the solution.
            human_report (str): A highly formatted string ready for terminal printing.
        """
        pass
