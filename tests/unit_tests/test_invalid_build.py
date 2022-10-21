import pytest
from magniv.build.build import build

from tests.unit_tests.fixtures.test_files import INVALID_KWARG_FILE, INVALID_TASK_KEY_FILE, INVALID_TRIGGER_FILE

# TODO: merge with TestBuild upon refactor there


class TestBuildInvalid:
    @pytest.fixture
    def folder(self, tmpdir, file):
        tmpdir.mkdir("tasks").join("main.py").write(file)
        tmpdir.join("tasks/requirements.txt").write("magniv")
        return str(tmpdir.join("tasks"))


class TestBuildInvalidKwarg(TestBuildInvalid):
    @pytest.fixture(scope="class")
    def file(self):
        return INVALID_KWARG_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTaskKey(TestBuildInvalid):
    @pytest.fixture(scope="class")
    def file(self):
        return INVALID_TASK_KEY_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTrigger(TestBuildInvalid):
    @pytest.fixture(scope="class")
    def file(self):
        return INVALID_TRIGGER_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)
