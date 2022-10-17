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
    """
    Creates a directory called tasks, creates a file called main.py in that directory, and writes
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


def test_invalid_kwarg_raises_error_on_build(file):
    with pytest.raises(ValueError):
        build(task_folder=file)
