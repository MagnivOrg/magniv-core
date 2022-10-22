import pytest

from magniv.build.build import build
from tests.unit_tests.fixtures.test_build import TestBuildInvalid
from tests.unit_tests.fixtures.test_files import (
    INVALID_KWARG_FILE,
    INVALID_TASK_KEY_FILE,
    INVALID_TRIGGER_FILE,
)


class TestBuildInvalidKwarg(TestBuildInvalid):
    @pytest.fixture
    def file(self):
        return INVALID_KWARG_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTaskKey(TestBuildInvalid):
    @pytest.fixture
    def file(self):
        return INVALID_TASK_KEY_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)


class TestBuildInvalidTrigger(TestBuildInvalid):
    @pytest.fixture
    def file(self):
        return INVALID_TRIGGER_FILE

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)
