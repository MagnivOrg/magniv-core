import pytest

class TestBuild:
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
    def file(self):
       """Method stub for test file"""
       pass