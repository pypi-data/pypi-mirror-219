from typing import Any, Callable, TypeVar, cast, Union, List, overload
import re
import importlib
import textwrap
import inspect
import warnings

import pytest

F = TypeVar("F", bound=Callable[..., Any])


def weight(value: float) -> Callable[[F], F]:
    """
    Add a weight for progress bar display
    """

    def decorator(func: F) -> F:
        cast(Any, func).weight = value
        return func

    return decorator


@overload
def full_version_only(__func: F) -> F:
    ...


@overload
def full_version_only(__name: str) -> Callable[[F], F]:
    ...


def full_version_only(func_or_name: Union[F, str]) -> Union[F, Callable[[F], F]]:
    """
    Mark a test as implemented in the full version only.

    May be called in two forms:

        @full_version_only
        def test_foo_bar():
            ...

        @full_version_only("module.name:function_name")
        def test_foo_bar():
            ...
    """

    def mismatch_placeholder(*args: Any) -> None:
        pytest.fail("**Version mismatch!** Could not find function implementation")

    def lite_version_placeholder(*args: Any) -> None:
        warnings.warn(
            textwrap.dedent(
                """\
                **Some tests were skipped.**

                Some tests are only available in the full version of Kevlar
                System Inspector.  Please contact `Star Lab`__ for more
                information.

                .. __: https://www.starlab.io/contact-us-kevlar-system-inspector-user
                """
            )
        )
        pytest.skip("not present")

    def get_params(func: Any) -> List[str]:
        return list(inspect.signature(func).parameters)

    def decorator(func: F) -> F:
        try:
            module = importlib.import_module(module_name)
            full_func = getattr(module, func_name, mismatch_placeholder)
        except ImportError:
            full_func = lite_version_placeholder
        else:
            # Import any fixtures defined in the implementation into the global
            # namespace, so it can use any full-version-only fixtures too.
            fixture_names = get_params(full_func)
            seen = set()
            while fixture_names:
                fixture_name = fixture_names.pop()
                if fixture_name in seen:
                    continue
                seen.add(fixture_name)

                fixture = getattr(module, fixture_name, None)
                if fixture is not None:
                    assert func.__globals__.get(fixture_name, fixture) is fixture, (
                        f"Internal: fixture name {fixture_name!r} in full version "
                        "would clobber current implmentation."
                    )
                    func.__globals__[fixture_name] = fixture

                    # Fixtures can use other fixtures...
                    fixture_names.extend(get_params(fixture))

        # Mark it for introspection
        full_func = pytest.mark.full_version_only(full_func)

        # Replace it wholesale so that pytest sees the fixtures of the the
        # implementation function, but copy over the documentation first so
        # that we don't have to duplicate. Other attributes are for unit
        # testing.
        full_func.__doc__ = func.__doc__
        full_func.__module__ = func.__module__
        full_func.__name__ = func.__name__
        full_func.__qualname__ = func.__qualname__
        return cast(F, full_func)

    if isinstance(func_or_name, str):
        assert ":" in func_or_name, "Expecting locator of the form 'module:function'"
        module_name, func_name = func_or_name.split(":", 1)
        return decorator
    else:
        func = func_or_name
        module_name = re.sub(
            r"\bkevlar_system_inspector\b",
            "kevlar_system_inspector_extras",
            func.__module__,
        )
        func_name = func.__name__
        return decorator(func)


def merge_tests(func: F) -> F:
    """
    Normally we show paramatrized tests as seperate tests. This will collect
    all issues under a single test instead.
    """
    cast(Any, func).merge_tests = True
    return func
