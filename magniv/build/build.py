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


def get_decorated_nodes(parsed_ast: ast.AST) -> List:
    """
    It returns a list of all function and async function definitions in the AST that have at least one
    decorator

    Args:
      parsed_ast (ast.AST): The parsed AST of the file.

    Returns:
      A list of nodes that are either a FunctionDef or AsyncFunctionDef and have a decorator_list.
    """
    return [
        node
        for node in ast.walk(parsed_ast)
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and len(node.decorator_list) > 0
        )
    ]


def get_magniv_tasks(
    filepath: str, decorated_nodes: List, root: str, req: str, used_keys: Dict
) -> Tuple[List, Dict]:
    """
    It returns all Magniv decorated tasks from a list of python functions that are decorated

    Args:
      filepath (str): The path to the file that contains the tasks.
      decorated_nodes (List): A list of all the nodes in the graph.
      root (str): The root directory of the project.
      req (str): The requirement file that is being parsed.
      used_keys (Dict): A dictionary of keys that have been used in the file.
    """
    tasks = []
    for node in decorated_nodes:
        core_values = {
            "location": filepath,
            "name": node.name,
            "python_version": _get_python_version(root),
            "owner": _get_owner(root),
            "requirements_location": req,
            "line_number": node.lineno,
            "key": node.name,
            "description": None,
        }
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Name) and decorator.func.id == "task":
                decorator_values = {kw.arg: kw.value.value for kw in decorator.keywords}
                info = {**core_values, **decorator_values}
                if missing_reqs := list({"schedule"} - set(info)):
                    raise ValueError(
                        "Task missing required variables, please resolve by defining ("
                        + ",".join([f" {x} " for x in missing_reqs])
                        + f') in the task decorator for function {info["name"]} at {info["location"]} line {info["line_number"]}'
                    )
                if info["key"] in used_keys:
                    raise ValueError(
                        f'Task "{info["key"]}" in file {filepath} is using "{info["key"]}" as a key which is already used in {used_keys[info["key"]]}, please resolve by changing one of the keys'
                    )
                used_keys[info["key"]] = filepath
                tasks.append(info)
    return tasks


def get_task_files(task_folder: str, reqs_pth: str, root_req: str) -> List:
    """
    > Get all the files in a task folder, including the files in the requirements folder

    Args:
      task_folder (str): the folder where the task is located
      reqs_pth (str): the path to the requirements.txt file
      root_req (str): The name of the root requirement file.
    """
    task_files = []
    for root, dirs, files in os.walk(task_folder):
        req = f"{root}/{reqs_pth}" if os.path.exists(f"{root}/{reqs_pth}") else root_req
        if req is None:
            raise OSError(
                f'requirements.txt not found for path "{root}", either add one to this directory or the root directory'
            )
        for file_name in files:
            if file_name.endswith(".py"):
                filepath = f"{root}/{file_name}"
                task_files.append(filepath)
    return task_files


def get_task_list(
    task_files: List,
    task_folder: str = None,
    req: str = None,
    tasks_list: List = None,
    used_keys: Dict = None,
) -> List:
    """
    "Get a list of tasks from a list of task files."

    Args:
      task_files (List): List of task files to be processed.
      task_folder (str): The folder where the tasks are located.
      req (str): The requirement file to be used.
      tasks_list (List): This is the list of tasks that will be returned.
      used_keys (Dict): A dictionary of keys that have already been used.
    """
    if tasks_list is None:
        tasks_list = []
    if used_keys is None:
        used_keys = {}
    for filepath in task_files:
        with open(filepath) as f:
            parsed_ast = ast.parse(f.read())
            decorated_nodes = get_decorated_nodes(parsed_ast)
            tasks_list.extend(
                get_magniv_tasks(
                    filepath, decorated_nodes, root=task_folder, req=req, used_keys=used_keys
                )
            )
    return tasks_list


def save_tasks(
    task_folder: str,
    save_dir: bool = False,
    dump_save_pth: str = "./dump.json",
    reqs_pth: str = "requirements.txt",
    tasks_list: List = None,
) -> NoReturn:
    """
    `save_tasks` saves a list of tasks to a file

    Args:
      task_folder (str): The folder where the tasks are located.
      save_dir (bool): If True, the directory of the task will be saved. Defaults to False
      dump_save_pth (str): The path to the file where the dump will be saved. Defaults to ./dump.json
      reqs_pth (str): The path to the requirements.txt file. Defaults to requirements.txt
      tasks_list (List): List = None
    """
    if not os.path.exists(f"{task_folder}/{reqs_pth}"):
        raise OSError(f"{task_folder}/{reqs_pth} not found")
    root_req = f"{task_folder}/{reqs_pth}"
    task_files = get_task_files(task_folder, reqs_pth, root_req)
    tasks_list = get_task_list(task_files, task_folder, root_req)
    if save_dir:
        dump_save_pth = task_folder + dump_save_pth[1:]
    _save_to_json(tasks_list, filepath=dump_save_pth)


def build(task_folder: str = None):
    """
    We walk through the `tasks` directory, and for each file we find, we check if it's a Python file,
    and if it is, we get the tasks from it and add them to our list of tasks
    """
    save_dir = False
    if task_folder is None:
        task_folder = "./tasks"
    else:
        save_dir = True
    if not os.path.exists(task_folder):
        raise OSError("You must have a tasks folder that contains all of your tasks files")

    # Hack to fix project imports by adding project directory to Python path
    sys.path.append(os.getcwd() + task_folder)
    save_tasks(task_folder, save_dir=save_dir)
