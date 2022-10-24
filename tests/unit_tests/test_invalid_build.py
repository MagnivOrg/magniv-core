import pytest

from magniv.build.build import build
from tests.unit_tests.fixtures.test_build import TestBuild
from tests.unit_tests.fixtures.test_files import (
    INVALID_KWARG_FILE,
    INVALID_TASK_KEY_FILE,
    INVALID_TRIGGER_FILE,
)

# TODO: merge with test_build file upon refactor there


class TestBuildInvalidKwarg(TestBuild):
    @pytest.fixture
    def file(self):
        return INVALID_KWARG_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTaskKey(TestBuild):
    @pytest.fixture
    def file(self):
        return INVALID_TASK_KEY_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTrigger(TestBuild):
    @pytest.fixture
    def file(self):
        return INVALID_TRIGGER_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)
