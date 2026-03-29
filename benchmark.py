import os

from src.genetic_algorithm import GeneticAlgorithm
from src.mtsp import MTSP

# --- EXPERIMENT CONFIGURATION ---
FIXED_GENS = 2000
FIXED_CROSS = 0.8
FIXED_ELITE = 1
NUM_WORKERS = 3
DEPOT = (30, 30)
CITIES = [
    (5, 10), (15, 25), (30, 5), (40, 20), (20, 40),
    (35, 35), (10, 30), (50, 45), (45, 10), (60, 30),
    (25, 15), (55, 20), (70, 10), (80, 25), (65, 40),
    (90, 30), (75, 50), (85, 15), (95, 35), (40, 50),
    (10, 5), (20, 25), (35, 10), (50, 15), (60, 5),
    (70, 20), (30, 50), (45, 25), (55, 35), (65, 15),
]

experiments = [
    {"pop": 50,  "mut": 0.05, "nome": "População Baixa + Mutação Baixa"},
    {"pop": 50,  "mut": 0.45, "nome": "População Baixa + Mutação Alta"},
    {"pop": 200, "mut": 0.05, "nome": "População Alta + Mutação Baixa"},
    {"pop": 200, "mut": 0.45, "nome": "População Alta + Mutação Alta"}
]

class SilentHistoryLogger:
    """
    A logger that silently collects generation data for the Mermaid charts 
    without polluting the terminal.
    """
    def __init__(self):
        self.history = []

    def print_header(self):
        pass # Do nothing silently

    def log(self, gen, max_fit, avg_fit, min_fit):
        self.history.append((gen, max_fit, avg_fit, min_fit))


def calc_convergence(history, best_fitness):
    for gen, max_fit, avg_fit, min_fit in history:
        # Use an error margin to avoid float issues in Python
        if max_fit >= best_fitness - 0.01:
            return gen
    return FIXED_GENS

def count_violations(fitness_score):
    if fitness_score > 0:
        return 0
    # If it's negative, each -100.000 is a violation (approximately)
    # We get the absolute value, add the V (10000) and divide by the multiplier
    return int((abs(fitness_score) + 10000) // 100000) + 1

def downsample_history(history, num_points=10):
    step = max(1, len(history) // num_points)
    sampled = history[::step]
    
    # Guarantees that the last point (final result) is in the graph
    if sampled[-1][0] != history[-1][0]:
        sampled.append(history[-1])
        
    return sampled

def main():
    print("🔬 Iniciando Bateria de Testes Automatizados...")
    
    # Guarantees that the /docs folder exists
    os.makedirs("docs", exist_ok=True)
    
    # Init the Markdown file
    md_content = "# Estudo de Hiperparâmetros\n\n"
    md_content += "Este documento foi gerado automaticamente através de testes empíricos do algoritmo genético.\n\n"
    
    # Table header
    md_content += "| Experimento | População | Mutação | Melhor Fitness | Convergência (Ger.) | Violações |\n"
    md_content += "| :--- | :---: | :---: | :---: | :---: | :---: |\n"
    
    mermaid_charts = ""

    for exp in experiments:
        print(f"\n⚙️  Rodando: {exp['nome']} (Pop: {exp['pop']}, Mut: {exp['mut']})")
        
        problem = MTSP(CITIES, DEPOT, num_workers=NUM_WORKERS)
        
        # Instantiate the silent logger to capture history
        history_logger = SilentHistoryLogger()
        
        ga = GeneticAlgorithm(
            population_size=exp["pop"],
            generations=FIXED_GENS,
            crossover_rate=FIXED_CROSS,
            mutation_rate=exp["mut"],
            elitism_count=FIXED_ELITE,
            logger=history_logger # Injects the logger here
        )
        
        # Run using the exact return signature of your updated GA
        solution, returned_violations, std_dev, best_fitness = ga.run(problem)
        
        # Retrieve the collected history from our custom logger
        history = history_logger.history
        
        # Extract metrics
        convergence_gen = calc_convergence(history, best_fitness)
        
        # We can calculate violations using the fitness formula or use the returned one.
        # Keeping the math inference as requested:
        computed_violations = count_violations(best_fitness) 
        
        # Fill the table row
        row = f"| {exp['nome']} | {exp['pop']} | {exp['mut']} | {best_fitness:.2f} | {convergence_gen} | {computed_violations} |\n"
        md_content += row
        print(f"✅ Concluído: Fitness {best_fitness:.2f} | Convergiu na gen {convergence_gen}")
        
        # Generate the Mermaid chart
        amostra = downsample_history(history, num_points=12)
        
        x_axis = [str(p[0]) for p in amostra] # Generations
        y_axis = [str(int(p[1])) for p in amostra] # Max Fitness converted to int
        
        # Mermaid requires square brackets without quotes for numeric arrays, so we format manually
        x_str = "[" + ", ".join(x_axis) + "]"
        y_str = "[" + ", ".join(y_axis) + "]"
        
        # The Y axis will dynamically change according to the fitness (or 10000 if negative)
        y_max = 10000 if best_fitness > 0 else 0
        y_min = int(amostra[0][1])
        
        mermaid_charts += f"### {exp['nome']}\n\n"
        mermaid_charts += "```mermaid\n"
        mermaid_charts += "xychart-beta\n"
        mermaid_charts += f"    title \"Evolução do Fitness — pop={exp['pop']}, mut={exp['mut']}\"\n"
        mermaid_charts += f"    x-axis \"Geração\" {x_str}\n"
        mermaid_charts += f"    y-axis \"Fitness\" {y_min} --> {y_max}\n"
        mermaid_charts += f"    line {y_str}\n"
        mermaid_charts += "```\n\n"

    # Join the table with the charts
    md_content += "\n## Gráficos de Convergência\n\n" + mermaid_charts
    
    # Save the file
    filepath = os.path.join("docs", "hiperparametros.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(md_content)
        
    print(f"\n🎉 Relatório gerado com sucesso em: {filepath}")

if __name__ == "__main__":
    main()
