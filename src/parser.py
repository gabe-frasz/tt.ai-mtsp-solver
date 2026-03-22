import argparse
import json
import os
import sys

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

def _load_config_file(filepath: str) -> dict:
    """
    Detects the file extension and loads the configuration file.
    """
    if not os.path.exists(filepath):
        print(f"Fatal Error: configuration file '{filepath}' not found.")
        sys.exit(1)

    _, ext = os.path.splitext(filepath)
    ext = ext.lower()

    if ext == ".json":
        with open(filepath, 'r') as f:
            return json.load(f)
    elif ext in [".yaml", ".yml"]:
        if not YAML_AVAILABLE:
            print("Fatal Error: PyYAML not installed. Run 'pip install pyyaml'.")
            sys.exit(1)
        with open(filepath, 'r') as f:
            return yaml.safe_load(f) or {}
    else:
        print(f"Fatal Error: Format '{ext}' not supported. Use .json or .yaml.")
        sys.exit(1)

def get_config() -> dict:
    """
    Builds the final configuration by resolving the hierarchy of truth:
    CLI Flags > Config File > Defaults
    """
    parser = argparse.ArgumentParser(description="mTSP Genetic Algorithm Solver")
    
    parser.add_argument("-c", "--config", type=str, help="Path to the configuration file (.json or .yaml)")
    
    parser.add_argument("-p", "--population", type=int, help="Population size")
    parser.add_argument("-g", "--generations", type=int, help="Number of generations")
    parser.add_argument("-x", "--crossover", type=float, help="Crossover rate (ex: 0.8)")
    parser.add_argument("-m", "--mutation", type=float, help="Mutation rate (ex: 0.05)")
    parser.add_argument("-e", "--elite", type=int, help="Quantity of elite individuals (the ones with the best fitness to survive)")

    # parser.add_argument("-w", "--workers", type=int, help="Quantity of workers (ex: 3)")
    
    args = parser.parse_args()

    # Defaults
    params = {
        "pop_size": 100,
        "generations": 1000,
        "crossover_rate": 0.8,
        "mutation_rate": 0.1,
        "elitism_count": 1,
        # "num_workers": 3
    }

    # Config file overrides defaults
    if args.config:
        file_params = _load_config_file(args.config)
        params.update(file_params)

    # CLI flags override config file and defaults
    for key, value in vars(args).items():
        if value is not None and key != "config":
            param_key_map = {
                "population": "pop_size",
                "generations": "generations", 
                "crossover": "crossover_rate",
                "mutation": "mutation_rate",
                "elite": "elitism_count",
                # "workers": "num_workers"
            }
            mapped_key = param_key_map.get(key, key)
            params[mapped_key] = value

    return params
