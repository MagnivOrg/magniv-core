import pytest

import ast
from typing import Union

class TestBuild:

    @pytest.fixture
    def file(self) -> str:
        """Must be implemented in subclass definition to return a test file as a string"""
        return ""

    @pytest.fixture
    def folder(self, tmp_path, file):
        """Uses the pytest builtin fixture tmp_path to create a temporary tasks folder and requirements.txt for each test invocation"""
        # setup tasks folder
        tasks_folder = tmp_path / "tasks"
        tasks_folder.mkdir()
        # write requirements.txt with magniv
        reqs = tasks_folder / "requirements.txt"
        reqs.write_text("magniv")
        # write contents of test file and return
        test_file = tasks_folder / "main.py"
        test_file.write_text(file)
        return str(tasks_folder)

    @pytest.fixture
    def ast(self, file) -> Union[ast.AST, str]:
        return ast.parse(file)
