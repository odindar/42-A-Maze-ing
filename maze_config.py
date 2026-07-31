#!/usr/bin/env python3


from dataclasses import dataclass
from typing import ClassVar


@dataclass
class MazeConfig:
    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    is_perfect: bool
    seed: int | None = None
    PATTERN_42: ClassVar[tuple[str, ...]] = (
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        )
