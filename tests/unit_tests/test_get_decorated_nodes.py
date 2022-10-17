import ast
import pytest
from typing import Union

from magniv.build.build import get_decorated_nodes

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

@dummydecorator
def dummy_task():
    print("This is a dummy task")
    return True

def dummy_task_2():
    print("This is a dummy task")
    return True

if __name__ == "__main__":
    hello_world()
"""


@pytest.fixture
def file(tmpdir):
    """
    It creates a directory called tasks, creates a file called main.py in that directory, and writes
    the contents of the TEST_FILE variable to that file. It then creates a file called
    requirements.txt in the tasks directory and writes the word magniv to it. Finally, it returns
    the path to the tasks directory

    Args:
        tmpdir: This is a pytest fixture that creates a temporary directory for us to use.

    Returns:
        The path to the directory where the file is located.
    """
    tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
    tmpdir.join("tasks/requirements.txt").write("magniv")
    return str(tmpdir.join("tasks"))


def get_ast(file) -> Union[ast.AST, str]:
    """
    It opens a file, reads it, and parses it into an AST
    :return: The parsed ast and the filepath
    """
    with open(f"{file}/main.py") as f:
        parsed_ast = ast.parse(f.read())
    return parsed_ast


def test_get_decorated_nodes_returns_all_magniv_aliases(file):
    parsed_ast = get_ast(file)
    nodes, aliases = get_decorated_nodes(parsed_ast)
    assert "magniv.core.task" in aliases
    assert "task" in aliases
    assert "mc.task" in aliases


def test_get_decorated_nodes_ignores_non_magniv_decorators(file):
    parsed_ast = get_ast(file)
    nodes, aliases = get_decorated_nodes(parsed_ast)
    assert "dummydecorator" not in aliases
