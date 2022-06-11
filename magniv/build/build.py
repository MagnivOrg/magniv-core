# Traverse all python files in this directory and one child lower as well.
import ast
import os
import platform
import sys
import pdb
from inspect import getsourcelines

from magniv.core import Task, task
from magniv.utils.utils import _save_to_json


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
                with open(filepath) as file:
                    parsed_ast = ast.parse(file.read())
                tasks = []
                for node in ast.walk(parsed_ast):
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        if len(node.decorator_list) > 0:
                            for decorator in node.decorator_list:
                                if not isinstance(decorator, ast.Name) and decorator.func.id == 'task':
                                    pdb.set_trace()
                                    tasks.append(node)
                for task in tasks:
                    tasks_list.append(task.name)
                print(tasks_list)
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
