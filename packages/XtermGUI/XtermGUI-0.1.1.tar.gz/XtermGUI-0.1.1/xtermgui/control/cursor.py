from __future__ import annotations
import sys
from .text import Text
from ..geometry import Coordinate


class Cursor:
    position = Coordinate(0, 0)

    @classmethod
    def up(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            return NotImplemented
        sys.__stdout__.write(f"\033[{n}A")
        sys.__stdout__.flush()
        cls.position -= (0, n)
        return cls

    @classmethod
    def down(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            return NotImplemented
        sys.__stdout__.write(f"\033[{n}B")
        sys.__stdout__.flush()
        cls.position += (0, n)
        return cls

    @classmethod
    def left(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            return NotImplemented
        sys.__stdout__.write(f"\033[{n}D")
        sys.__stdout__.flush()
        cls.position -= (n, 0)
        return cls

    @classmethod
    def right(cls, n: int = 1) -> type[Cursor]:
        if not isinstance(n, int):
            return NotImplemented
        sys.__stdout__.write(f"\033[{n}C")
        sys.__stdout__.flush()
        cls.position += (n, 0)
        return cls

    @classmethod
    def go_to(cls, coordinate: Coordinate | tuple[int, int]) -> type[Cursor]:
        if not isinstance(coordinate, (Coordinate, tuple)):
            return NotImplemented
        elif isinstance(coordinate, tuple) and tuple(map(type, coordinate)) != (int, int):
            return NotImplemented
        coordinate = coordinate if isinstance(coordinate, Coordinate) else Coordinate(*coordinate)
        sys.__stdout__.write(f"\033[{coordinate.y + 1};{coordinate.x + 1}H")
        sys.__stdout__.flush()
        cls.position = coordinate
        return cls

    @classmethod
    def update_position_on_print(cls, character: str) -> None:
        match character:
            case Text.ZERO_WIDTH:
                pass
            case Text.BACKSPACE:
                cls.position -= (1, 0)
            case Text.NEWLINE:
                cls.position = Coordinate(0, cls.position.y + 1)
            case Text.TAB:
                cls.position += (4, 0)
            case Text.CARRIAGE_RETURN:
                cls.position = Coordinate(0, cls.position.y)
            case Text.FORM_FEED:
                cls.position = Coordinate(cls.position.x + 1, cls.position.y + 1)
            case _:
                cls.position += (1, 0)
