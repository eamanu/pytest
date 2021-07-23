"""
Scope definition and related utilities.

Those are defined here, instead of in the 'fixtures' module because
their use is spread across many other pytest modules, and centralizing it in 'fixtures'
would cause circular references.

Also this makes the module light to import, as it should.
"""
from enum import Enum
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
        return _SCOPE_INDICES[self]

    def next(self) -> "Scope":
        """Return the next scope (from top to bottom)."""
        return _NEXT_SCOPES[self]

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

# Maps a high-level scope to its next scope. Function is absent here because it
# is the bottom-most scope.
_NEXT_SCOPES = {
    Scope.Session: Scope.Package,
    Scope.Package: Scope.Module,
    Scope.Module: Scope.Class,
    Scope.Class: Scope.Function,
}

# Maps a scope to its internal index, with Session = 0, Package = 1, and so on.
_SCOPE_INDICES = {s: i for i, s in enumerate(Scope)}
