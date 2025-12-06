from collections.abc import Callable
from dataclasses import dataclass
from re import Pattern
from typing import Any, Never, Protocol, cast


class Parser[T, C = None](Protocol):
    def parse(self, input_: str, *, context: C) -> T:
        raise NotImplementedError


@dataclass
class FnParser[T](Parser[T, None]):
    fn: Callable[[str], T] = lambda x: cast("T", x)

    def parse(self, input_: str, *, context=None):
        return self.fn(input_)


@dataclass
class IterableParser[T, C = None](Parser[list[T]]):
    line_parser: Parser[T, C]
    separator: str | Pattern = "\n"
    filter: Callable[[T], bool] | None = None

    def parse(self, input_: str, *, context: C = None) -> list[T]:
        res = [
            self.line_parser.parse(line, context=context)
            for line in (
                input_.split(self.separator)
                if isinstance(self.separator, str)
                else self.separator.split(input_)
            )
        ]
        if self.filter is not None:
            res = [v for v in res if self.filter(v)]
        return res


@dataclass
class MultiGroupsParser[GroupsData: tuple[Any, ...]](Parser[GroupsData, Never]):
    groups_parser: list[Parser[Any, list[Any]]]

    def parse(self, input_: str, *, context=None) -> GroupsData:
        res = []
        for group_parser, input_group in zip(
            self.groups_parser, input_.split("\n\n"), strict=True
        ):
            res.append(group_parser.parse(input_group, context=res))
        return res


def parse_int_pair(raw: str, *, separator="-") -> tuple[int, int]:
    a, b = raw.split(separator)
    return int(a), int(b)
