#!/usr/bin/env python3


from maze_config import MazeConfig


class MazeGenerator:
    def __init__(self, config: MazeConfig):
        self.config = config

        self.grid: list[list[int]] = [
            [15 for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]
        self.visited: list[list[bool]] = [
            [False for _ in range(self.config.width)]
            for _ in range(self.config.height)
        ]
        self._place_42_pattern()

    def _place_42_pattern(self) -> None:
        pattern = [
            "10001 0 11111",
            "10001 0 00001",
            "11111 0 11111",
            "00001 0 10000",
            "00001 0 11111"
        ]
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])
        if self.config.width < pattern_w + 2 or self.config.height < pattern_h + 2:
            return
        start_y = (self.config.height - pattern_h) // 2
        start_x = (self.config.width - pattern_w) // 2
        for y in range(pattern_h):
            for x in range(pattern_w):
                if pattern[y][x] == '1':
                    self.visited[start_y + y][start_x + x] = True

    def debug_print(self) -> None:
        for row in self.grid:
            print("".join(f"{cell:X}" for cell in row))
