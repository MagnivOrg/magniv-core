import pytest

from magniv.build.build import build
from tests.unit_tests.fixtures.test_build import TestBuild
from tests.unit_tests.fixtures.test_files import (
    INVALID_KWARG_FILE,
    INVALID_TASK_KEY_FILE,
    INVALID_TRIGGER_FILE,
)


class TestInvalidBuild(TestBuild):

    INVALID_TEST_FILE_LIST = [INVALID_KWARG_FILE, INVALID_TASK_KEY_FILE, INVALID_TRIGGER_FILE]

    @pytest.fixture(params=INVALID_TEST_FILE_LIST)
    def file(self, request):
        """
        Returns various invalid test files that are expected to fail when built.
        Add a file to above list to have it used for input to an instance of the test below
        """
        return request.param

    def test_invalid_build_raises_error(self, folder):
        with pytest.raises(ValueError):
            build(task_folder=folder)
