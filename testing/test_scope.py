import re

import pytest
from _pytest.scope import Scope


def test_index() -> None:
    assert Scope.Session.index() == 0
    assert Scope.Package.index() == 1
    assert Scope.Module.index() == 2
    assert Scope.Class.index() == 3
    assert Scope.Function.index() == 4


def test_next() -> None:
    assert Scope.Session.next() is Scope.Package
    assert Scope.Package.next() is Scope.Module
    assert Scope.Module.next() is Scope.Class
    assert Scope.Class.next() is Scope.Function

    with pytest.raises(ValueError):
        Scope.Function.next()


def test_from_user() -> None:
    assert Scope.from_user("module", "for parametrize", "some::id") is Scope.Module

    expected_msg = "for parametrize from some::id got an unexpected scope value 'foo'"
    with pytest.raises(pytest.fail.Exception, match=re.escape(expected_msg)):
        Scope.from_user("foo", "for parametrize", "some::id")  # type:ignore[arg-type]
