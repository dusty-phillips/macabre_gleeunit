import importlib
import inspect
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gleam_builtins import Error, Ok


def read_file(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return Ok(f.read())
    except Exception as error:
        return Error(error)


def main():
    from gleeunit.internal import reporting
    state = reporting.new_state()

    for module_name in gleam_test_modules():
        module = importlib.import_module(module_name)
        for function_name in dir(module):
            if not function_name.endswith("_test"):
                continue
            function = getattr(module, function_name)
            if not callable(function) or function.__module__ != module.__name__:
                continue
            try:
                signature = inspect.signature(function)
            except (TypeError, ValueError):
                signature = None
            if signature is not None and any(
                param.default is inspect.Parameter.empty
                for param in signature.parameters.values()
            ):
                continue
            try:
                function()
                state = reporting.test_passed(state)
            except (SystemExit, KeyboardInterrupt):
                raise
            except BaseException as error:
                print(f"\n--- {module_name}.{function_name} failed ---", file=sys.stderr)
                traceback.print_exception(type(error), error, error.__traceback__,
                                          file=sys.stderr)
                state = reporting.test_failed(state, module_name, function_name, error)

    sys.exit(reporting.finished(state))


def gleam_test_modules():
    # Discover compiled test modules next to this file (the build output
    # directory), not the project's test/ sources: modules skipped by the
    # compiler (no python implementation) have no .py output and must not be
    # imported. Only files ending in _test.py are entry candidates; helpers
    # (e.g. typecheck/helpers.py) are excluded by that suffix.
    root = os.path.dirname(os.path.abspath(__file__))
    modules = []
    for dirpath, dirnames, files in os.walk(root):
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for name in files:
            if not name.endswith("_test.py"):
                continue
            path = os.path.join(dirpath, name)
            relative = os.path.relpath(path, root)
            module = relative[: -len(".py")].replace(os.sep, ".")
            if module not in modules:
                modules.append(module)
    return sorted(modules)
