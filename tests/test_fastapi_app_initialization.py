import importlib
import sys


def test_fastapi_app_can_be_imported_and_initialized():
    """
    The FastAPI application module should be importable without errors.
    The ASGI app object should be accessible after import.
    This test fails if the module name is wrong (e.g. contains '.py' suffix
    or points to a non-existent module).
    """
    # The correct module name should NOT include '.py' extension.
    # Common conventions: 'main', 'app', 'fastapi_app', etc.
    # Based on the crash report the broken name was 'fastapi_error.py';
    # the correct module is expected to be 'main' or 'app'.
    # We test that a properly named module can be imported and exposes an app.

    # Try the most common FastAPI entry-point module names.
    candidate_modules = ['main', 'app', 'fastapi_app', 'application']

    imported_module = None
    for mod_name in candidate_modules:
        try:
            imported_module = importlib.import_module(mod_name)
            break
        except ModuleNotFoundError:
            continue

    assert imported_module is not None, (
        "Could not import any expected FastAPI application module. "
        "Ensure the entry-point module (e.g. 'main.py' or 'app.py') exists "
        "and does NOT include '.py' in the module reference string."
    )

    # The imported module should expose a FastAPI/ASGI app object.
    app = getattr(imported_module, 'app', None)
    assert app is not None, (
        f"Module '{imported_module.__name__}' was imported successfully but "
        "does not expose an 'app' attribute. "
        "Ensure the FastAPI instance is named 'app' at module level."
    )
