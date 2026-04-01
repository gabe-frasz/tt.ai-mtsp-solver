import importlib
import inspect
import os
import sys

from core.base_problem import BaseProblem


def problem_factory(problem_name: str, **kwargs):
    try:
        module = importlib.import_module(f"problems.{problem_name}")
    except (ImportError, ModuleNotFoundError):
        problems_dir = os.path.join(os.getcwd(), "problems")
        available = [
            f[:-3] for f in os.listdir(problems_dir) 
            if f.endswith(".py") and f != "__init__.py"
        ]
        print(f"FATAL ERROR: Problem '{problem_name}' not found.")
        print(f"Available valid problem names: {available}")
        sys.exit(1)

    for _, obj in inspect.getmembers(module):
        if (inspect.isclass(obj) and issubclass(obj, BaseProblem) and obj is not BaseProblem):
            return obj(**kwargs)

    print(f"FATAL ERROR: No BaseProblem subclass found in module '{problem_name}'.")
    sys.exit(1)
