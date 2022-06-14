# Traverse all python files in this directory and one child lower as well.
import ast
import os
import platform
import sys
from typing import Dict

from magniv.utils.utils import _save_to_json


def _get_python_version(root):
    """
    It returns the version of Python that is running

    :param root: The root directory of the project
    :return: The version of Python that is being used.
    """
    return platform.python_version()


def _get_owner(root):
    """
    It returns the string "local"

    :param root: The root directory of the project
    :return: The owner of the root directory.
    """
    return "local"


def get_tasks_from_file(filepath, root, req, used_keys) -> Dict:
    """
    > This function takes a filepath, root, req, and used_keys as arguments and returns a dictionary of
    tasks and used_keys

    :param filepath: The path to the file that contains the task
    :param root: The root directory of the project
    :param req: The location of the requirements.txt file
    :param used_keys: This is a dictionary of keys that have been used so far. This is used to ensure
    that no two tasks have the same key
    :return: A list of dictionaries, each dictionary is a task.
    """
    with open(filepath) as file:
        parsed_ast = ast.parse(file.read())
        tasks = []
        for node in ast.walk(parsed_ast):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if len(node.decorator_list) > 0:
                    for decorator in node.decorator_list:
                        if not isinstance(decorator, ast.Name) and decorator.func.id == "task":
                            for decorator in node.decorator_list:
                                info = {
                                    "location": filepath,
                                    "name": node.name,
                                    "python_version": _get_python_version(root),
                                    "owner": _get_owner(root),
                                    "requirements_location": req,
                                    "line_number": node.lineno,
                                    "key": node.name,
                                    "description": None,
                                }
                                for kw in decorator.keywords:
                                    info[kw.arg] = kw.value.value
                                missing_reqs = list({"schedule"} - set(info))
                                if len(missing_reqs) > 0:
                                    raise ValueError(
                                        "Task missing required variables, please resolve by defining ("
                                        + ",".join([f" {x} " for x in missing_reqs])
                                        + ") in the task decorator"
                                    )
                                if info["key"] in used_keys:
                                    raise ValueError(
                                        f'Task "{info["key"]}" in file {filepath} is using "{info["key"]}" as a key which is already used in {used_keys[info["key"]]}, please resolve by changing one of the keys'
                                    )
                                else:
                                    used_keys[info["key"]] = filepath
                                tasks.append(info)
        return tasks, used_keys


def build():
    """
    We walk through the `tasks` directory, and for each file we find, we check if it's a Python file,
    and if it is, we get the tasks from it and add them to our list of tasks
    """
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
        req = (
            "{}/requirements.txt".format(root)
            if os.path.exists("{}/requirements.txt".format(root))
            else root_req
        )
        if req == None:
            raise OSError(
                f'requirements.txt not found for path "{root}", either add one to this directory or the root directory'
            )
        for file_name in files:
            ext = os.path.splitext(file_name)[-1].lower()
            if ext == ".py":
                filepath = "{}/{}".format(root, file_name)
                tasks, used_keys = get_tasks_from_file(filepath, root, req, used_keys)
                tasks_list.extend(tasks)
        _save_to_json(tasks_list, filepath="./dump.json")
