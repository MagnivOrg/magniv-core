import pytest

class TestBuildInvalid:
    @pytest.fixture
    def folder(self, tmpdir, file):
        tmpdir.mkdir("tasks").join("main.py").write(file)
        tmpdir.join("tasks/requirements.txt").write("magniv")
        return str(tmpdir.join("tasks"))
