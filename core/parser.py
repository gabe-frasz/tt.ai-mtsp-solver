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
    Builds the final configuration using the configuration file as the 
    Single Source of Truth.
    """
    parser = argparse.ArgumentParser(description="Multi-Problem Solver using Genetic Algorithm")
    parser.add_argument("-c", "--config", type=str, help="Path to the configuration file (.json or .yaml)")
    args = parser.parse_args()

    config_path = args.config

    # Fallback
    if not config_path:
        if os.path.exists("config.yaml"):
            config_path = "config.yaml"
        elif os.path.exists("config.yml"):
            config_path = "config.yml"
        elif os.path.exists("config.json"):
            config_path = "config.json"

    if not config_path:
        print("Fatal Error: No configuration file provided and default 'config.yaml/yml/json' not found.")
        sys.exit(1)

    config = _load_config_file(config_path)

    # Ensure the required blocks exist
    if not all(key in config for key in ["ga_config", "problem_name", "problem_config"]):
        print(f"Fatal Error: Configuration file '{config_path}' is missing required blocks (ga_config, problem_name, problem_config).")
        sys.exit(1)

    return config
