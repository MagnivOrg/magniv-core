import hashlib
import importlib.util
import os
import sys


def run(filepath, function_name):
    """
    It imports a Python file and runs a function from it

    :param filepath: The path to the file containing the function to be run
    :param function_name: The name of the function to run
    :return: The return value of the function.
    """
    org_mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
    path_hash = hashlib.sha1(filepath.encode("utf-8")).hexdigest()
    mod_name = f"unusual_prefix_{path_hash}_{org_mod_name}"
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    # Hack to fix project imports by adding project directory to Python path
    sys.path.append(f"{os.getcwd()}/tasks")
    spec.loader.exec_module(mod)
    func = getattr(mod, function_name)
    return func()
