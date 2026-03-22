# mTSP Solver - Genetic Algorithm

This project implements a **Multiple Travelling Salesman Problem (mTSP)** solver using a **Genetic Algorithm (GA)** in Python. The goal is to optimize the routes of multiple salesmen (workers) who must visit a set of cities, starting and returning to a central depot, while minimizing total distance and balancing the workload.

## 📋 Problem Description

- **Salesmen:** 3 workers.
- **Cities:** 30 cities with fixed coordinates.
- **Depot:** Central office located at (30, 30).
- **Goal:** Minimize total distance traveled by all workers and minimize the standard deviation of distances between workers.
- **Constraints:**
  - Each city must be visited exactly once.
  - Every worker must visit between 5 and 15 cities.
  - The difference between the number of cities assigned to any two workers cannot exceed 5.
  - No worker's total distance can exceed 350 units.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/tt.ai-mtsp-solver.git
   cd tt.ai-mtsp-solver
   ```

2. **(Optional) Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/bin/activate  # Linux/macOS
   ```

3. **Install dependencies:**
   *(Optional)* If you want to use YAML configuration files:
   ```bash
   pip install pyyaml
   ```

## 🚀 Execution

Run the solver using the default parameters:
```bash
python3 main.py
```

### Configuration via CLI Flags

You can override parameters directly from the command line:
```bash
python3 main.py -p 200 -g 500 -m 0.1 -w 3
```

**Available flags:**
- `-p, --population`: Population size (default: 100).
- `-g, --generations`: Number of generations (default: 1000).
- `-m, --mutation`: Mutation rate (0.0 to 1.0).
- `-x, --crossover`: Crossover rate (0.0 to 1.0).
- `-e, --elite`: Number of elite individuals to preserve.
- `-c, --config`: Path to a `.json` or `.yaml` configuration file.

### Output Example

The program will output the complete route for each worker, the individual distances, the total distance, the standard deviation, and any constraint violations found.

## 📂 Project Structure

- `src/`: Source code containing the GA logic, problem definition, and utilities.
- `main.py`: Entry point for the application.
- `docs/`: Technical documentation (modelagem and hiperparametros).
