import ast
from pathlib import Path


GATED_IMAGE_FUNCTIONS = {
    "gallery_ai_upscale",
    "gallery_style_transfer",
    "inpaint_proxy",
    "harmonize_image",
    "denoise_image",
    "upscale_image_local",
    "remove_background",
    "enhance_face",
}


def _gallery_source():
<<<<<<< HEAD
    return Path("routes/gallery_routes.py").read_text(encoding="utf-8")
=======
    return Path("routes/gallery/gallery_routes.py").read_text(encoding="utf-8")
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483


def _function_sources(source):
    tree = ast.parse(source)
    return {
        node.name: ast.get_source_segment(source, node) or ""
        for node in ast.walk(tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_image_generation_endpoints_require_image_privilege():
    source = _gallery_source()
    functions = _function_sources(source)

    for name in GATED_IMAGE_FUNCTIONS:
        assert name in functions
        assert 'require_privilege(request, "can_generate_images")' in functions[name]


def test_gallery_routes_imports_privilege_helper():
<<<<<<< HEAD
    assert "from src.auth_helpers import get_current_user, require_privilege" in _gallery_source()
=======
    source = _gallery_source()
    assert "get_current_user" in source
    assert "require_privilege" in source
>>>>>>> 9d0d3720f4ca181d87bef94da826d730acc6d483
