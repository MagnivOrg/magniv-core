import pytest

from magniv.build.build import get_decorated_nodes
from tests.build_tests.fixtures.test_build import TestBuild
from tests.build_tests.fixtures.test_files import GET_DECORATED_NODES_FILE


class TestGetDecoratedNodes(TestBuild):
    @pytest.fixture
    def file(self):
        """returns a file that contains multiple types of valid decorators"""
        return GET_DECORATED_NODES_FILE

    def test_get_decorated_nodes_returns_all_magniv_aliases(self, ast):
        nodes, aliases = get_decorated_nodes(ast)
        assert "magniv.core.task" in aliases
        assert "task" in aliases
        assert "mc.task" in aliases

    def test_get_decorated_nodes_ignores_non_magniv_decorators(self, ast):
        nodes, aliases = get_decorated_nodes(ast)
        assert "dummydecorator" not in aliases
