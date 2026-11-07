"""Regression guard for issue #1414 — a broken upstream `searxng:latest` tag
(2026.6.2 crashed on boot with KeyError: 'default_doi_resolver') failed the
searxng healthcheck, and because `odysseus` waits on it via
`depends_on: condition: service_healthy`, the whole app never started on fresh
Docker installs.

Pin the SearXNG image to a known-good tag so a bad upstream `latest` can't block
startup. This guards that the pin stays in place.
"""
import re
from pathlib import Path

<<<<<<< HEAD
COMPOSE = Path(__file__).resolve().parent.parent / "docker-compose.yml"
=======
import yaml

ROOT = Path(__file__).resolve().parent.parent
COMPOSE = ROOT / "docker-compose.yml"
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483


def test_searxng_image_is_pinned_not_latest():
    text = COMPOSE.read_text(encoding="utf-8")
<<<<<<< HEAD
    m = re.search(r"image:\s*\S*searxng/searxng:(\S+)", text)
    assert m, "searxng image line not found in docker-compose.yml"
    tag = m.group(1)
    assert tag != "latest", (
        "SearXNG must be pinned, not ':latest' — odysseus startup depends on its "
        "healthcheck, so a broken upstream latest tag blocks the app (issue #1414)"
    )
    # A real version tag (date-based, e.g. 2026.5.31-7159b8aed), not a moving ref.
    assert re.match(r"\d{4}\.\d", tag), f"expected a versioned tag, got {tag!r}"
=======
    image = yaml.safe_load(text)["services"]["searxng"]["image"]
    assert re.fullmatch(
        r"docker\.io/searxng/searxng:\d{4}\.\d[^\s@]*@sha256:[0-9a-f]{64}", image
    ), f"SearXNG must use a versioned immutable upstream image: {image!r}"


def test_all_standalone_compose_files_select_the_same_searxng_image():
    expected = yaml.safe_load(COMPOSE.read_text())["services"]["searxng"]["image"]
    for name in ("docker-compose.gpu-amd.yml", "docker-compose.gpu-nvidia.yml"):
        actual = yaml.safe_load((ROOT / name).read_text())["services"]["searxng"]["image"]
        assert actual == expected, f"{name} selects a different SearXNG image"
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
