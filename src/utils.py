import math


class Utils:
    @staticmethod
    def calc_euclidean_distance(coord1: tuple[int, int], coord2: tuple[int, int]):
        """
        Calculates the Euclidean distance between two coordinates.
        """
        dx = abs(coord1[0] - coord2[0])
        dy = abs(coord1[1] - coord2[1])
        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def calc_std_dev(data: list[float]):
        """
        Calculates the standard deviation of a list of numbers.
        """
        if not data: return 0.0
        n = len(data)
        mean = sum(data) / n
        variance = sum((x - mean) ** 2 for x in data) / n
        return math.sqrt(variance)
