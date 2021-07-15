"""
Scope definition and related utilities.

Those are defined here, instead of in the 'fixtures', module because
their use is spread across many other pytest modules, and centralizing it in 'fixtures'
would cause circular references.

Also this makes the module light to import, as it should.
"""
from enum import Enum
from functools import lru_cache
from typing import Optional
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Literal

    _ScopeName = Literal["session", "package", "module", "class", "function"]


class Scope(Enum):
    """Represents one of the possible fixture scopes in pytest."""

    Session = "session"
    Package = "package"
    Module = "module"
    Class = "class"
    Function = "function"

    def index(self) -> int:
        """Return this scope index. Smaller numbers indicate higher scopes (Session = 0)."""
        return _scope_to_index(self)

    def next(self) -> "Scope":
        """Return the next scope (from top to bottom)."""
        return _next_scope(self)

    @classmethod
    def from_user(
        cls, scope_name: "_ScopeName", descr: str, where: Optional[str] = None
    ) -> "Scope":
        """
        Given a scope name from the user, return the equivalent Scope enum. Should be used
        whenever we want to convert a user provided scope name to its enum object.

        If the scope name is invalid, construct a user friendly message and call pytest.fail.
        """
        from _pytest.outcomes import fail

        try:
            return Scope(scope_name)
        except ValueError:
            fail(
                "{} {}got an unexpected scope value '{}'".format(
                    descr, f"from {where} " if where else "", scope_name
                ),
                pytrace=False,
            )


# Ordered list of scopes which can contain many tests (in practice all except Function).
HIGH_SCOPES = [x for x in Scope if x is not Scope.Function]


@lru_cache(maxsize=None)
def _scope_to_index(scope: Scope) -> int:
    """Implementation of Scope.index() as a free function so we can cache it."""
    scopes = list(Scope)
    return scopes.index(scope)


@lru_cache(maxsize=None)
def _next_scope(scope: Scope) -> Scope:
    """Implementation of Scope.next() as a free function so we can cache it."""
    if scope is Scope.Function:
        raise ValueError("Function is the bottom scope")
    scopes = list(Scope)
    index = scopes.index(scope)
    return scopes[index + 1]
