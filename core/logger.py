class GALogger:
    def __init__(self, total_generations: int, step: int = 20):
        self.total = total_generations
        self.step = max(1, total_generations // step)

    def print_header(self):
        print(f"{'Gen':>5} | {'Max Fitness':>12} | {'Avg Fitness':>12} | {'Min Fitness':>12}")
        print("-" * 51)

    def log(self, gen: int, max_fit: float, avg_fit: float, min_fit: float):
        # Print progress at a regular interval and at the end
        if gen % self.step == 0 or gen == self.total - 1:
            print(f"{gen:5d} | {max_fit:12.2f} | {avg_fit:12.2f} | {min_fit:12.2f}")
