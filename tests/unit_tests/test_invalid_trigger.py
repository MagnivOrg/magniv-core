import pytest

from magniv.build.build import build

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


@pytest.fixture
def file(tmpdir):
    tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
    tmpdir.join("tasks/requirements.txt").write("magniv")
    return str(tmpdir.join("tasks"))

def test_invalid_trigger_parameter_raises_error_on_build(file):
    with pytest.raises(ValueError):
        build(task_folder=file)
