#!/usr/bin/env python3

import random
from collections import deque
from maze_config import MazeConfig

DIRECTIONS = {
    "N": (-1, 0, 1, 4),
    "S": (1, 0, 4, 1),
    "E": (0, 1, 2, 8),
    "W": (0, -1, 8, 2),
}


class MazeGenerator:
    def __init__(self, config: MazeConfig):
        self.config = config

        self.grid: list[list[int]] = [
            [15 for _ in range(self.config.width)] for _ in range(self.config.height)
        ]
        self.visited: list[list[bool]] = [
            [False for _ in range(self.config.width)] for _ in range(self.config.height)
        ]
        self._place_42_pattern()

    def _place_42_pattern(self) -> None:
        pattern = [
            "1000111",
            "1000001",
            "1110111",
            "0010100",
            "0010111",
        ]
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])
        if self.config.width < pattern_w + 2 or self.config.height < pattern_h + 2:
            return
        start_y = (self.config.height - pattern_h) // 2
        start_x = (self.config.width - pattern_w) // 2
        for y in range(pattern_h):
            for x in range(pattern_w):
                if pattern[y][x] == "1":
                    self.visited[start_y + y][start_x + x] = True

    def _get_unvisited_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors = []
        for direction, (dy, dx, _, _) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.config.width and 0 <= ny < self.config.height:
                if not self.visited[ny][nx]:
                    neighbors.append((direction, nx, ny))
        return neighbors

    def generate(self) -> None:
        if hasattr(self.config, "seed") and self.config.seed is not None:
            random.seed(self.config.seed)
        start_x, start_y = self.config.entry
        self.visited[start_y][start_x] = True
        stack: list[tuple[int, int]] = [(start_x, start_y)]
        while stack:
            current_x, current_y = stack[-1]
            neighbors = self._get_unvisited_neighbors(current_x, current_y)
            if neighbors:
                direction, next_x, next_y = random.choice(neighbors)
                _, _, bit_current, bit_next = DIRECTIONS[direction]
                self.grid[current_y][current_x] -= bit_current
                self.grid[next_y][next_x] -= bit_next
                self.visited[next_y][next_x] = True
                stack.append((next_x, next_y))
            else:
                stack.pop()


    def _solve_maze(self) -> str:
        entry: tuple[int, int] = self.config.entry
        exit: tuple[int, int] = self.config.exit

        if entry == exit:
            return ""
        queue = deque([(entry[0], entry[1], "")])
        visited: set = set()
        visited.add(entry)

        while queue:
            cx, cy, path = queue.popleft()
            if (cx, cy) == exit:
                return path

            cur_value = self.grid[cy][cx]
            for direction_char, (dy, dx, wall_bit, _) in DIRECTIONS.items():
                if (cur_value & wall_bit) == 0:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.config.width and 0 <= ny < self.config.height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            queue.append((nx, ny, path + direction_char))
        return ""


    def save_to_file(self) -> None:
        try:
            with open(self.config.output_file, "w") as f:
                for row in self.grid:
                    hex_row = "".join(f"{cell:X}" for cell in row)
                    f.write(f"{hex_row}\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                # TODO: Henüz yolu bulmadık, o yüzden şimdilik yer tutucu koyuyoruz.
                path = self._solve_maze()
                f.write(f"{path}\n")
        except Exception as e:
            print(f"Error writing to output file: {e}")

    def debug_print(self) -> None:
        for row in self.grid:
            print("".join(f"{cell:X}" for cell in row))
