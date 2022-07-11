import ast
import os
from typing import Union

import pytest

from tests.unit_tests.test_build import TestBuild

from magniv.build.build import (
    build,
    get_decorated_nodes,
    get_magniv_tasks,
    get_task_files,
    get_task_list,
    save_tasks,
)

TEST_FILE = """from datetime import datetime

import magniv
from magniv.core import task
from magniv import core as mc


@magniv.core.task(schedule="@hourly", description="Hello world, printing the time", key="goodbye_world_1")
def hello_world():
    print(f"Hello world, the time is {datetime.now()}")

@task(schedule="@daily", description="Hello world, printing a second time", key="goodbye_world_2")
def hello_world_2():
    print(f"Hello world, the time is {datetime.now()}")

@mc.task(schedule="@daily", description="Hello world, printing a third time", key="goodbye_world_3")
def hello_world_3():
    print(f"Hello world, the time is {datetime.now()}")


def dummy_task():
    print("This is a dummy task")
    return True

if __name__ == "__main__":
    hello_world()
"""


class TestBuild(TestBuild):
    @pytest.fixture
    def file(self, tmpdir):
        tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
        tmpdir.join("tasks/requirements.txt").write("magniv")
        return str(tmpdir.join("tasks"))

    def _extracted_from_test_get_decorated_nodes(self, decorated_nodes, arg1, arg2, arg3, arg4):
        assert decorated_nodes[arg1].name == arg2
        assert decorated_nodes[arg1].decorator_list[0].keywords[0].arg == "schedule"
        assert decorated_nodes[arg1].decorator_list[0].keywords[0].value.s == arg3
        assert decorated_nodes[arg1].decorator_list[0].keywords[2].value.s == arg4

    def test_get_decorated_nodes(self, file):
        """
        `get_decorated_nodes` returns a list of all the decorated functions in a Python file
        """
        parsed_ast, filepath = self.get_ast(file)
        decorated_nodes, _ = get_decorated_nodes(parsed_ast)
        self._extracted_from_test_get_decorated_nodes(
            decorated_nodes, 0, "hello_world", "@hourly", "goodbye_world_1"
        )
        self._extracted_from_test_get_decorated_nodes(
            decorated_nodes, 1, "hello_world_2", "@daily", "goodbye_world_2"
        )
        self._extracted_from_test_get_decorated_nodes(
            decorated_nodes, 2, "hello_world_3", "@daily", "goodbye_world_3"
        )
