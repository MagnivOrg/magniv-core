import ast

import pytest

from magniv.build.build import (
    get_decorated_nodes,
    get_task_files,
    get_tasks_from_file,
    save_tasks,
)


class TestBuild:
    def get_ast(self):
        filepath = "tests/unit_tests/test_build_helper.py"
        with open(filepath) as f:
            parsed_ast = ast.parse(f.read())
        return parsed_ast, filepath

    def test_get_decorated_nodes(self):
        parsed_ast, filepath = self.get_ast()
        decorated_nodes = get_decorated_nodes(parsed_ast)
        assert decorated_nodes[0].name == "hello_world"
        assert decorated_nodes[0].decorator_list[0].func.id == "task"
        assert decorated_nodes[0].decorator_list[0].keywords[0].arg == "schedule"
        assert decorated_nodes[0].decorator_list[0].keywords[0].value.s == "@hourly"

    def test_get_tasks_from_file(self):
        parsed_ast, filepath = self.get_ast()
        decorated_nodes = get_decorated_nodes(parsed_ast)
        tasks, used_keys = get_tasks_from_file(
            filepath,
            decorated_nodes,
            root="tests/unit_tests",
            req="requirements.txt",
            used_keys={},
        )
        assert tasks[0]["name"] == "hello_world"
        assert tasks[0]["schedule"] == "@hourly"
        assert tasks[0]["location"] == "tests/unit_tests/test_build_helper.py"
        assert tasks[0]["requirements_location"] == "requirements.txt"
        assert tasks[0]["description"] == "Hello world, printing the time"
        assert used_keys["hello_world"] == "tests/unit_tests/test_build_helper.py"

    def test_reqs_dependency(self):
        with pytest.raises(OSError):
            save_tasks(task_folder="")

    @pytest.fixture
    def reqs_filepath(self, tmpdir):
        tmpdir.mkdir("tasks").join("requirements.txt").write("")
        return str(tmpdir.join("tasks"))

    def test_reqs_filepath(self, reqs_filepath):
        with pytest.raises(TypeError):
            save_tasks(task_folder=reqs_filepath)

    @pytest.fixture
    def subdir_reqs_filepath(self, tmpdir):
        tmpdir.mkdir("tasks").mkdir("subdir").mkdir("subsubdir").join("requirements.txt").write(
            ""
        )
        return str(tmpdir.join("tasks/subdir/subsubdir"))

    def test_subdirreqs_filepath(self, subdir_reqs_filepath):
        with pytest.raises(TypeError):
            save_tasks(task_folder=subdir_reqs_filepath)
