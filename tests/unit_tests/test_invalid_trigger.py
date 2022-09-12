import ast
import os
from typing import Union

import pytest

from magniv.build.build import (
    build,
    get_decorated_nodes,
    get_magniv_tasks,
    get_task_files,
    get_task_list,
    save_tasks,
)

TEST_FILE = """from datetime import datetime

from magniv.core import task

trigger_lst = ['task_b']

@task(schedule="@daily", _on_success=trigger_lst)
def task_a():
    print("I")

@task()
def task_b():
    print("i'm only triggered by task A")


if __name__ == "__main__":
    hello_world()
"""


class TestBuild:
    @pytest.fixture
    def file(self, tmpdir):
        tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
        tmpdir.join("tasks/requirements.txt").write("magniv")
        return str(tmpdir.join("tasks"))

    def test_build(self, file):
        """
        `build` is a function that takes a filepath and a task_folder argument and saves all the tasks
        in that folder to a file

        :param file: a filepath to a Python file
        """
        json_pth = f"{file}/dump.json"
        with pytest.raises(ValueError):
            build(task_folder=file)