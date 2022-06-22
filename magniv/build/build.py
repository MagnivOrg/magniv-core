# Traverse all python files in this directory and one child lower as well.
import ast
import os
import platform
import sys
from typing import Dict, List, NoReturn, Tuple

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


def get_tasks_from_file(filepath: str, root: str, req: str, used_keys: Dict) -> Tuple[List, Dict]:
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
    tasks = []
    with open(filepath) as file:
        parsed_ast = ast.parse(file.read())
    decorated_nodes = [
        node
        for node in ast.walk(parsed_ast)
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and len(node.decorator_list) > 0
        )
    ]
    for node in decorated_nodes:
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Name) and decorator.func.id == "task":
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


def save_tasks(
    task_folder: str,
    dump_save_pth: str = "./dump.json",
    reqs_pth: str = "requirements.txt",
    root_req: None = None,
    tasks_list: List = [],
    used_keys: Dict = {},
) -> NoReturn:
    """
    Save the decorated tasks to a json file.

    :param task_folder: The folder where the tasks are located
    :param dump_save_pth: The path to the file where the dump will be saved, defaults to ./dump.json
    :param reqs_pth: The path to the requirements.txt file, defaults to /requirements.txt
    :param root_req: The root requirement file to use, defaults to None
    :param tasks_list: The list of tasks to save, defaults to []
    :param used_keys: The dictionary of used keys, defaults to {}
    :return: NoReturn
    """
    for root, dirs, files in os.walk(task_folder):
        if os.path.exists(f"{task_folder}/{reqs_pth}"):
            root_req = task_folder + reqs_pth
        req = f"{root}/{reqs_pth}" if os.path.exists(f"{root}/{reqs_pth}") else root_req
        if req is None:
            raise OSError(
                f'requirements.txt not found for path "{root}", either add one to this directory or the root directory'
            )
        for file_name in files:
            ext = os.path.splitext(file_name)[-1].lower()
            if ext == ".py":
                filepath = f"{root}/{file_name}"
                tasks, used_keys = get_tasks_from_file(filepath, root, req, used_keys)
                tasks_list.extend(tasks)
        _save_to_json(tasks_list, filepath=dump_save_pth)


def build():
    """
    We walk through the `tasks` directory, and for each file we find, we check if it's a Python file,
    and if it is, we get the tasks from it and add them to our list of tasks
    """
    task_folder = "./tasks"
    if not os.path.exists(task_folder):
        raise OSError("You must have a tasks folder that contains all of your tasks files")

    # Hack to fix project imports by adding project directory to Python path
    sys.path.append(os.getcwd() + task_folder)
    save_tasks(task_folder)
