import ast
from typing import Union

from tests.unit_tests.fixtures.test_files import GET_DECORATED_NODES_FILE
from tests.unit_tests.test_invalid_build import TestBuildInvalid

import pytest

from magniv.build.build import get_decorated_nodes

class TestDecoratedNodes():

    @pytest.fixture
    def ast(self) -> Union[ast.AST, str]:
        return ast.parse(GET_DECORATED_NODES_FILE)

    def test_get_decorated_nodes_returns_all_magniv_aliases(self, ast):
        nodes, aliases = get_decorated_nodes(ast)
        assert "magniv.core.task" in aliases
        assert "task" in aliases
        assert "mc.task" in aliases


    def test_get_decorated_nodes_ignores_non_magniv_decorators(self, ast):
        nodes, aliases = get_decorated_nodes(ast)
        assert "dummydecorator" not in aliases
