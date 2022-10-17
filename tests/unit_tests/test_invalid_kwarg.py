import pytest

from magniv.build.build import build

TEST_FILE = """from datetime import datetime

from magniv.core import task

@task(schedule="@daily", bad=True)
def task_a():
    print("I")


if __name__ == "__main__":
    hello_world()
"""


@pytest.fixture
def file(tmpdir):
    tmpdir.mkdir("tasks").join("main.py").write(TEST_FILE)
    tmpdir.join("tasks/requirements.txt").write("magniv")
    return str(tmpdir.join("tasks"))

def test_invalid_kwarg_raises_error_on_build(file):
    with pytest.raises(ValueError):
        build(task_folder=file)
