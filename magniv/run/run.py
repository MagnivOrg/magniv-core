import sys
import importlib.util
import hashlib
import os
import json


def run(filepath, function_name):
    org_mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
    path_hash = hashlib.sha1(filepath.encode("utf-8")).hexdigest()
    mod_name = f"unusual_prefix_{path_hash}_{org_mod_name}"
    spec = importlib.util.spec_from_file_location(mod_name, filepath)
    mod = importlib.util.module_from_spec(spec)
    # Hack to fix project imports by adding project directory to Python path
    sys.path.append(os.getcwd() + "/tasks")
    spec.loader.exec_module(mod)
    func = getattr(mod, function_name)
    return func()
