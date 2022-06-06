# Traverse all python files in this directory and one child lower as well.
import os
from inspect import getmembers, getsourcelines
from magniv.core import task, Task
from magniv.utils.utils import _save_to_json
import importlib.util
import hashlib
import platform
import sys


def _get_python_version(root):
    return platform.python_version()


def _get_owner(root):
    return "local"


def build():
    is_task = lambda x: isinstance(x, Task)
    tasks_list = []
    used_keys = {}
    root_req = None
    if not os.path.exists("./tasks"):
        raise OSError("You must have a tasks folder that contains all of your tasks files")

    # Hack to fix project imports by adding project directory to Python path
    sys.path.append(os.getcwd() + "/tasks")

    for root, dirs, files in os.walk("./tasks"):
        if os.path.exists("./tasks/requirements.txt"):
            root_req = "./tasks/requirements.txt"
        for file_name in files:
            ext = os.path.splitext(file_name)[-1].lower()
            if ext == ".py":
                filepath = "{}/{}".format(root, file_name)
                org_mod_name, _ = os.path.splitext(os.path.split(filepath)[-1])
                path_hash = hashlib.sha1(filepath.encode("utf-8")).hexdigest()
                mod_name = f"unusual_prefix_{path_hash}_{org_mod_name}"
                spec = importlib.util.spec_from_file_location(mod_name, filepath)
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                tasks = getmembers(mod, is_task)
                req = (
                    "{}/requirements.txt".format(root)
                    if os.path.exists("{}/requirements.txt".format(root))
                    else root_req
                )
                if req == None:
                    raise OSError(
                        f'requirements.txt not found for path "{root}", either add one to this directory or the root directory'
                    )
                for name, t in tasks:
                    if t.key in used_keys:
                        raise ValueError(
                            f'Task "{t.key}" in file {filepath} is using "{t.key}" as a key which is already used in {used_keys[t.key]}, please resolve by changing one of the keys'
                        )
                    else:
                        used_keys[t.key] = filepath
                    code, lineno = getsourcelines(t)
                    info = {
                        "location": filepath,
                        "name": t.name,
                        "key": t.key,
                        "description": t.description,
                        "schedule": t.schedule,
                        "python_version": _get_python_version(root),
                        "owner": _get_owner(root),
                        "requirements_location": req,
                        "line_number": lineno,
                    }
                    tasks_list.append(info)
        _save_to_json(tasks_list, filepath="./dump.json")
