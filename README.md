# Universal Genetic Algorithm Hub

A decoupled framework for solving complex combinatorial optimization problems using Genetic Algorithms.
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

Run the solver using the default `config.yaml`:
```bash
python3 main.py
```

To use a custom configuration file:
```bash
python3 main.py --config custom_config.yaml
```

## 📂 Supported Problems

Detailed documentation for each supported problem can be found in the [docs/problems/](./docs/problems/) folder.

- [Multiple Traveling Salesperson Problem (mTSP)](./docs/problems/mtsp.md)
