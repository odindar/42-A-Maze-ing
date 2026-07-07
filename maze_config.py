#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Tuple, Optional

@dataclass
class MazeConfig:
    width: int
    height: int
    entry: Tuple[int, int]
    exit: Tuple[int, int]
    output_file: str
    perfect: bool
    seed: Optional[int] = None
