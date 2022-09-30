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
