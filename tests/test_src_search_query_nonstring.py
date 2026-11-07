<<<<<<< HEAD
import importlib.machinery
import importlib.util
from pathlib import Path


_PATH = Path(__file__).resolve().parents[1] / "src" / "search" / "query.py"


def _load():
    loader = importlib.machinery.SourceFileLoader("odysseus_src_search_query", str(_PATH))
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


def test_src_search_helpers_handle_non_string_queries():
    q = _load()

=======
"""Query helpers must tolerate non-string input.

`src.search.query` is a compatibility shim that aliases the canonical
`services.search.query`, so this exercises the live implementation.
"""
import services.search.query as q


def test_query_helpers_handle_non_string_queries():
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    assert q._detect_question_type(None) is None
    assert q._split_multi_part(None) == []
    assert q._extract_site_filter(None) == ("", None)
    assert q._is_news_query(None) is False
    assert isinstance(q.enhance_query(None)[0], str)
    assert isinstance(q.build_enhanced_query(123), str)


<<<<<<< HEAD
def test_src_search_valid_query_still_works():
    q = _load()

=======
def test_query_valid_query_still_works():
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    assert q._detect_question_type("who is bob") == "who"
    assert q._is_news_query("latest news today") is True
    assert q._extract_site_filter("cats site:x.com")[1] == "x.com"
