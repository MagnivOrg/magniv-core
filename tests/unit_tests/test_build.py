import ast
import os
from typing import Union

import pytest

# fmt: off
from magniv.build.build import (build, get_decorated_nodes, get_magniv_tasks, get_task_files,
                                get_task_list, save_tasks)

# fmt: on

TEST_FILE = """from datetime import datetime

from magniv.core import task


@task(schedule="@hourly", description="Hello world, printing the time")
def hello_world():
    print(f"Hello world, the time is {datetime.now()}")


def dummy_task():
    print("This is a dummy task")
    return True

if __name__ == "__main__":
    hello_world()
"""


class TestBuild:
    @pytest.fixture
    def file(self, tmpdir):
        tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
        tmpdir.join("tasks/requirements.txt").write("magniv")
        return str(tmpdir.join("tasks"))

    def get_ast(self, file) -> Union[ast.AST, str]:
        """
        It opens a file, reads it, and parses it into an AST
        :return: The parsed ast and the filepath
        """
        with open(f"{file}/main.py") as f:
            parsed_ast = ast.parse(f.read())
        return parsed_ast, file

    def test_get_decorated_nodes(self, file):
        """
        `get_decorated_nodes` returns a list of all the decorated functions in a Python file
        """
        parsed_ast, filepath = self.get_ast(file)
        decorated_nodes = get_decorated_nodes(parsed_ast)
        assert decorated_nodes[0].name == "hello_world"
        assert decorated_nodes[0].decorator_list[0].func.id == "task"
        assert decorated_nodes[0].decorator_list[0].keywords[0].arg == "schedule"
        assert decorated_nodes[0].decorator_list[0].keywords[0].value.s == "@hourly"

    def test_get_magniv_tasks(self, file):
        """
        It takes a filepath, parses the file, finds all the decorated functions, and returns a list of
        dictionaries containing the information about each task
        """
        parsed_ast, filepath = self.get_ast(file)
        decorated_nodes = get_decorated_nodes(parsed_ast)
        used_keys = {}
        tasks = get_magniv_tasks(
            filepath,
            decorated_nodes,
            root="tests/unit_tests",
            req="requirements.txt",
            used_keys=used_keys,
        )
        assert tasks[0]["name"] == "hello_world"
        assert tasks[0]["schedule"] == "@hourly"
        assert tasks[0]["location"] == filepath
        assert tasks[0]["requirements_location"] == "requirements.txt"
        assert tasks[0]["description"] == "Hello world, printing the time"
        assert used_keys["hello_world"] == filepath

    def test_get_tasklist(self, file):
        """
        It takes a filepath, parses the file, finds all the decorated functions, and returns a list of
        dictionaries containing the information about each task
        """
        task_list = get_task_list([f"{file}/main.py"])
        assert task_list[0]["name"] == "hello_world"
        assert task_list[0]["schedule"] == "@hourly"
        assert task_list[0]["location"] == f"{file}/main.py"
        assert task_list[0]["requirements_location"] is None
        assert task_list[0]["description"] == "Hello world, printing the time"

    def test_get_task_files(self, file):
        """
        `get_task_files` is a function that takes a folder path as an argument and returns a list of
        filepaths to all the files in that folder
        """
        task_files = get_task_files(
            file, "requirements.txt", root_req=f"{str(file)}/requirements.txt"
        )
        assert task_files[0] == f"{file}/main.py"

    def test_save(self, file):
        """
        `save_tasks` is a function that takes a folder path as an argument and saves all the tasks in
        :param file: This is the path to the folder where the tasks are stored
        """
        json_pth = f"{file}/dump.json"
        save_tasks(task_folder=file, dump_save_pth=json_pth)
        assert os.path.exists(json_pth) is True

    def test_build(self, file):
        """
        `build` is a function that takes a filepath and a task_folder argument and saves all the tasks
        in that folder to a file

        :param file: a filepath to a Python file
        """
        json_pth = f"{file}/dump.json"
        build(task_folder=file)
        assert os.path.exists(json_pth) is True
        with pytest.raises(OSError):
            build(task_folder="")

    def test_reqs_dependency(self):
        """
        > This function tests that the save_tasks function raises an OSError if the task_folder argument
        is an empty string
        """
        with pytest.raises(OSError):
            save_tasks(task_folder="")

    @pytest.fixture
    def subdir_reqs_file(self, tmpdir):
        """
        It creates a directory structure with a requirements.txt file in it

        :param tmpdir: This is a pytest fixture that creates a temporary directory for us to use
        :return: The path to the requirements.txt file.
        """
        tmpdir.mkdir("tasks").mkdir("subdir").mkdir("subsubdir").join("requirements.txt").write(
            "magniv"
        )
        return str(tmpdir.join("tasks/subdir/subsubdir"))

    def test_subdirreqs_filepath(self, subdir_reqs_file):
        """
        `save_tasks` is a function that takes a folder path as an argument and saves all the tasks in
        that folder to a file

        :param subdir_reqs_file: a filepath to a requirements.txt file in a subdirectory
        """
        json_pth = f"{subdir_reqs_file}/dump.json"
        save_tasks(task_folder=subdir_reqs_file, dump_save_pth=json_pth)
        assert os.path.exists(json_pth) == True
