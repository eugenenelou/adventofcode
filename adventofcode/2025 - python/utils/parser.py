from collections.abc import Callable
from dataclasses import dataclass
from typing import Any, Never, Protocol, cast


class Parser[T, C = None](Protocol):
    def parse(self, input_: str, *, context: C) -> T:
        raise NotImplementedError

@dataclass
class FnParser[T](Parser[T, None]):
    fn: Callable[[str], T] = lambda x: cast('T', x)

    def parse(self, input_:str, *,context = None):
        return self.fn(input_)

@dataclass
class IterableParser[T, C = None](Parser[list[T]]):
    line_parser: Parser[T, C]
    separator: str = "\n"

    def parse(self, input_:str,*, context: C = None) -> list[T]:
        return [self.line_parser.parse(line, context=context) for line in input_.split(self.separator)]

@dataclass
class MultiGroupsParser[GroupsData: tuple[Any, ...]](Parser[GroupsData, Never]):
    groups_parser: list[Parser[Any, list[Any]]]

    def parse(self, input_: str, *, context=None) -> GroupsData:
        res = [None]
        for group_parser, input_group in zip(self.groups_parser, input_.split('\n\n'), strict=True) :
            res.append(group_parser.parse(input_group, context=res))
        return res