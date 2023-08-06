from typing import Any, Callable, Generic, NoReturn, Optional, Tuple, TypeVar


def rraise(_: Any) -> NoReturn:
    raise NotImplementedError


INITIAL_T = TypeVar("INITIAL_T")
FINAL_T = TypeVar("FINAL_T")

NEW_FINAL_T = TypeVar("NEW_FINAL_T")


class Pipe(Generic[INITIAL_T, FINAL_T]):
    def __init__(self, func: Callable[[INITIAL_T], FINAL_T]) -> None:
        self.func = func

    def __rshift__(self, other: Callable[[FINAL_T], NEW_FINAL_T]) -> "Pipe[INITIAL_T, NEW_FINAL_T]":
        return Pipe(lambda value: other(self.func(value)))

    def __call__(self, value: INITIAL_T) -> FINAL_T:
        return self.func(value)

    def pipe(self, other: Callable[[FINAL_T], NEW_FINAL_T]) -> "Pipe[INITIAL_T, NEW_FINAL_T]":
        return Pipe(lambda value: other(self.func(value)))


T = TypeVar("T")
J = TypeVar("J")
PREDICATE = Callable[[T], bool]
TRANSFORMER = Callable[[T], J]


def pattern_match(
    cases: Tuple[Tuple[PREDICATE[T], TRANSFORMER[T, J]], ...],
    default: Optional[TRANSFORMER[T, J]] = None,
) -> Pipe[T, J]:
    @Pipe
    def _pattern_match(value: T) -> J:
        for case, transform in cases:
            if case(value):
                return transform(value)

        if default is not None:
            return default(value)
        raise ValueError("No case matched")

    return _pattern_match
