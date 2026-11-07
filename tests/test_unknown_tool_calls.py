import sys
from unittest.mock import MagicMock

<<<<<<< HEAD
# Clean up any mocks from previous tests to ensure we load real modules
for mod in ['src.agent_tools', 'src.tool_parsing', 'src.tool_schemas', 'src.tool_execution']:
    sys.modules.pop(mod, None)

# Mock heavy database/model dependencies before importing
for mod in [
    'sqlalchemy', 'sqlalchemy.orm', 'sqlalchemy.ext', 'sqlalchemy.ext.declarative',
    'sqlalchemy.ext.hybrid', 'sqlalchemy.sql', 'sqlalchemy.sql.expression',
    'src.database', 'core.models', 'core.database', 'core.auth'
]:
    if mod not in sys.modules:
        sys.modules[mod] = MagicMock()

import pytest
import src.agent_tools
from src.tool_parsing import parse_tool_blocks
from src.tool_schemas import function_call_to_tool_block
from src.tool_execution import execute_tool_block
from types import SimpleNamespace
=======
# This module needs the real agent-tool stack; importing it pulls in heavy
# DB/auth deps, so we stub those just long enough to import, then restore them.
# We deliberately do NOT pop src.tool_execution: popping and re-importing it
# rebinds the `src` package's `tool_execution` attribute, so a later
# `import src.tool_execution as te` resolves to a different module object than
# the one its functions live in - which silently breaks tests that monkeypatch
# it (e.g. test_edit_file's admin gate).
_ABSENT = object()
_AGENT_MODULES = ["src.agent_tools", "src.tool_parsing", "src.tool_schemas"]
_STUBBED = [
    "sqlalchemy", "sqlalchemy.orm", "sqlalchemy.ext", "sqlalchemy.ext.declarative",
    "sqlalchemy.ext.hybrid", "sqlalchemy.sql", "sqlalchemy.sql.expression",
    "src.database", "core.models", "core.database", "core.auth",
]
_saved_stubs = {name: sys.modules.get(name, _ABSENT) for name in _STUBBED}

for _mod in _AGENT_MODULES:
    sys.modules.pop(_mod, None)
for _mod in _STUBBED:
    if _mod not in sys.modules:
        sys.modules[_mod] = MagicMock()

import pytest  # noqa: E402
import src.agent_tools  # noqa: E402,F401
from src.tool_parsing import parse_tool_blocks  # noqa: E402
from src.tool_schemas import function_call_to_tool_block  # noqa: E402

# Drop the stubs we installed so they do not leak into later tests.
for _name, _original in _saved_stubs.items():
    if _original is _ABSENT:
        sys.modules.pop(_name, None)
    else:
        sys.modules[_name] = _original
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483


def test_parse_xml_unknown_tool_returns_none():
    """XML-style <invoke> tags with truly unknown tools should be filtered out (return None)."""
    text = '<invoke name="super_secret_tool"><parameter name="arg1">value1</parameter></invoke>'
    blocks = parse_tool_blocks(text)
    assert len(blocks) == 0


def test_parse_tool_call_unknown_tool_returns_none():
    """[TOOL_CALL] blocks with truly unknown tools should be filtered out (return None)."""
    text = '[TOOL_CALL] {tool => "mega_blast", command => "run energy"} [/TOOL_CALL]'
    blocks = parse_tool_blocks(text)
    assert len(blocks) == 0


def test_function_call_to_tool_block_unknown_tool_returns_none():
    """Native function calls of truly unknown tools should return None."""
    block = function_call_to_tool_block("ultra_zap", '{"power": 9000}')
    assert block is None


def test_function_call_to_tool_block_invalid_json_returns_none():
    """Unparseable JSON arguments should result in returning None."""
    block = function_call_to_tool_block("web_search", '{"query": "valid json')  # invalid JSON
    assert block is None


def test_google_search_mapping():
    """google_search should map to web_search and extract the first query from queries list or string."""
    # List of queries case
    block = function_call_to_tool_block("google_search", '{"queries": ["testing google search"]}')
    assert block is not None
    assert block.tool_type == "web_search"
    assert block.content == "testing google search"

    # Single string query case
    block = function_call_to_tool_block("google_search_retrieval", '{"queries": "testing google search string"}')
    assert block is not None
    assert block.tool_type == "web_search"
    assert block.content == "testing google search string"
