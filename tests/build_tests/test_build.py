import ast
import os
from typing import Union

import pytest

from magniv.build.build import (
    build,
    get_decorated_nodes,
    get_magniv_tasks,
    get_task_files,
    get_task_list,
    save_tasks,
)
from tests.build_tests.fixtures.test_build import TestBuild
from tests.build_tests.fixtures.test_files import VALID_TEST_FILE

# FIXME: make this use base class from fixtures dir


class TestValidBuild(TestBuild):
    @pytest.fixture
    def file(self):
        return VALID_TEST_FILE

    def test_valid_build_saves_dump_json(self, folder):
        expected_json_path = f"{folder}/dump.json"
        build_result = build(task_folder=folder)
        assert os.path.exists(expected_json_path)

    # TODO: isolate tasklist oriented tests in a separate class or file

    def test_get_tasklist(self, folder):
        """
        It takes a filepath, parses the file, finds all the decorated functions, and returns a list of
        dictionaries containing the information about each task
        """
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        assert task_list[0]["name"] == "hello_world"
        assert task_list[0]["schedule"] == "@hourly"
        assert task_list[0]["location"] == f"{folder}/main.py"
        assert task_list[0]["requirements_location"] is None
        assert task_list[0]["description"] == "Hello world, printing the time"

    def test_get_task_files(self, folder):
        """
        `get_task_files` is a function that takes a folder path as an argument and returns a list of
        filepaths to all the files in that folder
        """
        task_files = get_task_files(
            folder,
        )
        assert task_files[0]["filepath"] == f"{folder}/main.py"

    def test_save(self, folder):
        """
        `save_tasks` is a function that takes a folder path as an argument and saves all the tasks in
        :param file: This is the path to the folder where the tasks are stored
        """
        expected_dump_json_path = f"{folder}/dump.json"
        save_tasks(task_folder=folder, dump_save_pth=expected_dump_json_path)
        assert os.path.exists(expected_dump_json_path) is True

    def test_reqs_dependency(self):
        """
        > This function tests that the save_tasks function raises an OSError if the task_folder argument
        is an empty string
        """
        with pytest.raises(OSError):
            save_tasks(task_folder="")

    @pytest.fixture
    def subdir_reqs_file(self, tmpdir):
        """
        It creates a directory structure with a requirements.txt file in it

        :param tmpdir: This is a pytest fixture that creates a temporary directory for us to use
        :return: The path to the requirements.txt file.
        """
        tmpdir.mkdir("tasks").mkdir("subdir").mkdir("subsubdir").join("requirements.txt").write(
            "magniv"
        )
        return str(tmpdir.join("tasks/subdir/subsubdir"))

    def test_subdirreqs_filepath(self, subdir_reqs_file):
        """
        `save_tasks` is a function that takes a folder path as an argument and saves all the tasks in
        that folder to a file

        :param subdir_reqs_file: a filepath to a requirements.txt file in a subdirectory
        """
        json_pth = f"{subdir_reqs_file}/dump.json"
        save_tasks(task_folder=subdir_reqs_file, dump_save_pth=json_pth)
        assert os.path.exists(json_pth) == True

    def test_task_builds_with_valid_custom_resources(self, folder):
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        for task in task_list:
            if task["name"] == "resourceful_valid":
                assert task["resources"] == {
                    "limit_cpu": "500mi",
                    "limit_memory": "3Gi",
                }

    def test_task_ignores_invalid_custom_resources(self, folder):
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        for task in task_list:
            if task["name"] == "resourceful_invalid":
                assert not task["resources"]

    def test_task_builds_with_webhook_trigger_enabled(self, folder):
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        for task in task_list:
            if task["name"] == "playing_webhooky":
                assert task["webhook_trigger"]

    def test_task_builds_without_schedule(self, folder):
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        for task in task_list:
            if task["name"] == "task_b":
                assert not task["schedule"]
            elif task["name"] == "c":
                assert not task["schedule"]

    def test_task_builds_with_on_success(self, folder):
        task_list = get_task_list([{"filepath": f"{folder}/main.py", "req": None}])
        for task in task_list:
            if task["name"] == "task_a":
                assert task["on_success"] == ["task_b", "c"]
            if task["name"] == "task_b":
                assert task["is_called_by"] == ["task_a", "c"]
            if task["name"] == "c":
                assert task["is_called_by"] == ["task_a"]
                assert task["webhook_trigger"]
