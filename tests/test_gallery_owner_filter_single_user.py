<<<<<<< HEAD
"""_owner_filter must not blank out the gallery in single-user mode.

When AUTH_ENABLED=false, get_current_user returns None. The gallery main
list and stats treat None as "show all images" (`if user is not None`), but
_owner_filter returned q.filter(False) (zero rows) for None. So the tag and
model filter chips were always empty and clear-user-tags / clear-ai-tags /
dedupe-tags silently no-oped. _owner_filter must match the main list: no
filter when user is None, owner-scoped otherwise.
"""
import tempfile
import uuid

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

import core.database as cdb
from core.database import GalleryImage
from routes.gallery_helpers import _owner_filter

_TMPDB = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
_ENGINE = create_engine(f"sqlite:///{_TMPDB.name}", connect_args={"check_same_thread": False}, poolclass=NullPool)
cdb.Base.metadata.create_all(_ENGINE)
_TS = sessionmaker(bind=_ENGINE, autoflush=False, autocommit=False)
=======
"""_owner_filter must separate single-user mode from anonymous callers.

When AUTH_ENABLED=false, get_current_user returns None and gallery routes should
stay all-visible. When AUTH_ENABLED=true and no current user resolves, the same
None means an anonymous caller and gallery queries must fail closed.
"""
import uuid
import sys

import pytest
from tests.helpers.database import disposable_database

from core.database import GalleryImage
from routes.gallery_helpers import _owner_filter


@pytest.fixture(autouse=True)
def _gallery_database(tmp_path):
    with disposable_database(tmp_path) as factory:
        with pytest.MonkeyPatch.context() as patcher:
            patcher.setattr(sys.modules[__name__], "_TS", factory, raising=False)
            yield
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483


def _seed(*owners):
    db = _TS()
    try:
        db.query(GalleryImage).delete()
        for o in owners:
            db.add(GalleryImage(id=str(uuid.uuid4()), filename=f"{uuid.uuid4().hex}.png", owner=o))
        db.commit()
    finally:
        db.close()


<<<<<<< HEAD
def test_none_user_returns_all_rows():
=======
def test_none_user_returns_all_rows(monkeypatch):
    monkeypatch.setenv("AUTH_ENABLED", "false")
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
    _seed(None, None, "alice")
    db = _TS()
    try:
        n = _owner_filter(db.query(GalleryImage), None).count()
        assert n == 3  # old code returned 0
    finally:
        db.close()


def test_named_user_is_still_scoped():
    _seed("alice", "alice", "bob", None)
    db = _TS()
    try:
        assert _owner_filter(db.query(GalleryImage), "alice").count() == 2
        assert _owner_filter(db.query(GalleryImage), "bob").count() == 1
    finally:
        db.close()
<<<<<<< HEAD
=======


def test_none_user_blocks_when_auth_is_enabled(monkeypatch):
    monkeypatch.setenv("AUTH_ENABLED", "true")
    _seed(None, "alice", "bob")
    db = _TS()
    try:
        assert _owner_filter(db.query(GalleryImage), None).count() == 0
    finally:
        db.close()
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
