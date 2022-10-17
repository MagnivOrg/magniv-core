import pytest

from magniv.build.build import build

TEST_FILE = """from datetime import datetime

from magniv.core import task

@task(schedule="@daily", on_success=['task_b', 'bad_key'])
def task_a():
    print("I")

@task()
def task_b():
    print("i'm only triggered by task A")

@task(key="task_c")
def bad_key():
    print("i'm only triggered by task A")


if __name__ == "__main__":
    hello_world()
"""



@pytest.fixture
def file(tmpdir):
    tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
    tmpdir.join("tasks/requirements.txt").write("magniv")
    return str(tmpdir.join("tasks"))

def test_invalid_task_key_raises_error_on_build(file):
    with pytest.raises(ValueError):
        build(task_folder=file)
