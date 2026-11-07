"""Regression guards for in-chat document deep-links (#document-<id>).

The frontend module is browser-coupled (window/fetch/document) so there's
no JS unit harness for it — these pin the source-level invariants that the
404-silent-failure fix depends on. See issue #560.
"""

from pathlib import Path
<<<<<<< HEAD
=======
from tests.helpers.document_source import document_source
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483

_REPO = Path(__file__).resolve().parents[1]


def test_chat_document_links_use_the_document_id():
    """The list/open tool must anchor to the real document id, not a slug —
    a slug 404s against the UUID-keyed /api/document/<id> route."""
<<<<<<< HEAD
    src = (_REPO / "src" / "tool_implementations.py").read_text(encoding="utf-8")
=======
    src = (_REPO / "src" / "agent_tools" /"document_tools.py").read_text(encoding="utf-8")
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    assert "(#document-{d.id})" in src
    assert "(#document-{doc.id})" in src


def test_document_deeplink_handled_on_hashchange_and_load():
    """#document-<id> in the URL must open the doc on refresh / URL-bar nav,
    not just on click."""
<<<<<<< HEAD
    js = (_REPO / "static" / "js" / "document.js").read_text(encoding="utf-8")
=======
    js = document_source()
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    assert "addEventListener('hashchange', _maybeOpenDocFromHash)" in js
    assert "#document-" in js


def test_failed_document_load_surfaces_user_error():
    """A missing/failed document must tell the user, not fail silently."""
<<<<<<< HEAD
    js = (_REPO / "static" / "js" / "document.js").read_text(encoding="utf-8")
=======
    js = document_source()
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    assert "uiModule.showError" in js
    assert "Document not found" in js
