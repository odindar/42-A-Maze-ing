import random
from collections import deque

from maze_config import MazeConfig

DIRECTIONS = {
    "N": (-1, 0, 1, 4),
    "E": (0, 1, 2, 8),
    "S": (1, 0, 4, 1),
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
        pattern = MazeConfig.PATTERN_42
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])

        if self.config.width < pattern_w + 2 or self.config.height < pattern_h + 2:
            return

        start_y = self.config.height // 2 - (pattern_h // 2)
        start_x = self.config.width // 2 - (pattern_w // 2)

        for y in range(pattern_h):
            for x in range(pattern_w):
                if pattern[y][x] == "1":
                    self.visited[start_y + y][start_x + x] = True

    def _get_unvisited_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors: list[str, int, int] = []
        for direction, (dy, dx, _, _) in DIRECTIONS.items():
            nx, ny = x + dx, y + dy
            if (
                0 <= nx < self.config.width
                and 0 <= ny < self.config.height
                and not self.visited[ny][nx]
            ):
                neighbors.append((direction, nx, ny))
        return neighbors

    def generate(self) -> None:
        if hasattr(self.config, "seed") and self.config.seed != None:
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

        if not self.config.is_perfect:
            self._make_imperfect()

    def _solve_maze(self) -> str:
        entry: tuple[int, int] = self.config.entry
        exit: tuple[int, int] = self.config.exit

        if entry == exit:
            return ""

        queue = deque([(entry[0], entry[1], "")])
        self.visited = [[False for _ in range(self.config.width)] for _ in range(self.config.height)]
        self.visited[entry[1]][entry[0]] = True

        while queue:
            cx, cy, path = queue.popleft()
            if (cx, cy) == exit:
                return path

            cur_value: int = self.grid[cy][cx]
            for direction_char, (dy, dx, wall_bit, _) in DIRECTIONS.items():
                if (cur_value & wall_bit) == 0:
                    nx, ny = cx + dx, cy + dy
                    if (
                        0 <= nx < self.config.width
                        and 0 <= ny < self.config.height
                        and not self.visited[ny][nx]
                    ):
                        self.visited[ny][nx] = True
                        queue.append((nx, ny, path + direction_char))
        return ""

    def _make_imperfect(self) -> None:
        DEAD_END = {7, 11, 13, 14}

        queue: deque = deque()

        for y in range(self.config.height):
            for x in range(self.config.width):
                if self.grid[y][x] in DEAD_END:
                    queue.append((x, y))

        while queue:
            x, y = queue.popleft()

            if self.grid[y][x] not in DEAD_END:
                continue

            candidates: list[tuple[int, int, int, int]] = [
                (x + dx, y + dy, bc, bn)
                for _, (dy, dx, bc, bn) in DIRECTIONS.items()
                if (
                    0 <= x + dx < self.config.width
                    and 0 <= y + dy < self.config.height
                    and self.grid[y + dy][x + dx] != 15
                    and self.grid[y][x] & bc
                )
            ]
            if not candidates:
                continue

            nx, ny, bc, bn = random.choice(candidates)
            self.grid[y][x]   -= bc
            self.grid[ny][nx] -= bn

    def save_to_file(self) -> None:
        try:
            with open(self.config.output_file, "w") as f:
                for row in self.grid:
                    hex_row = "".join(f"{cell:X}" for cell in row)
                    f.write(f"{hex_row}\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                path: str = self._solve_maze()
                f.write(f"{path}\n")
        except Exception as e:
            print(f"Error writing to output file: {e}")
