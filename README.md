# Universal Genetic Algorithm Hub

A decoupled framework for solving complex combinatorial optimization problems using [Genetic Algorithms](https://en.wikipedia.org/wiki/Genetic_algorithm).
This hub is designed with architectural integrity, featuring lazy-loading problem discovery and
a clear separation between the GA engine and problem domains.

## 🚀 Key Features

- **Decoupled Architecture**: The GA engine is completely agnostic of the problem being solved.
- **Lazy Loading**: Problems are discovered and loaded dynamically via convention-over-configuration.
- **Single Source of Truth**: All configurations (GA hyperparameters and problem-specific data) are managed via a central YAML/JSON file.
- **Extensible**: Easily add new problems by inheriting from `BaseProblem`.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/fr.genetic-algorithm-hub.git
   cd fr.genetic-algorithm-hub
   ```

2. **Set up the environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Linux/macOS
   ```

3. **Install dependencies:**
   ```bash
   pip install pyyaml
   ```

## 📋 Quickstart

Run the solver using the default `config.yaml` (if present):
```bash
python3 main.py
```

To use a custom configuration file:
```bash
python3 main.py --config custom_config.yaml
```

## ⚙️ Configuration

The engine is universally controlled by the `config.yaml` file located in the root directory.
You don't need to touch the Python code to tune the Genetic Algorithm. 

The configuration file is divided into three main blocks: `ga_config`, `problem_name`, and `problem_config`.

The `ga_config` block is entirely agnostic and dictates the behavior of the evolutionary engine:

| Parameter | Type | Description |
| :--- | :---: | :--- |
| `pop_size` | `int` | The number of individuals (chromosomes) in each generation. Larger populations explore the search space better but take longer to compute. |
| `generations` | `int` | The maximum number of evolutionary cycles the engine will run before stopping and returning the best found solution. |
| `crossover_rate` | `float` | The probability (0.0 to 1.0) of two selected parents mating to produce offspring. High rates encourage mixing of good traits. |
| `mutation_rate` | `float` | The probability (0.0 to 1.0) of a gene mutating. Essential for maintaining genetic diversity and preventing the algorithm from getting stuck in local optima. |
| `elitism_count` | `int` | The absolute number of the absolute best individuals that are guaranteed to survive to the next generation without undergoing crossover or mutation. |

The `problem_name` block specifies the name of the file of the problem to be solved
and the `problem_config` block contains the problem-specific parameters.

*Note: To see the specific `problem_config` parameters required for each domain,
please refer to the individual problem documentation below.*

## 📂 Supported Problems

Detailed documentation for each supported problem can be found in the [docs/problems/](./docs/problems/) folder.

- [Multiple Traveling Salesperson Problem (mTSP)](./docs/problems/mtsp.md)
