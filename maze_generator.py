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

        start_y = self.config.height // 2 - 2
        start_x = self.config.width // 2 - 3

        for y in range(pattern_h):
            for x in range(pattern_w):
                if pattern[y][x] == "1":
                    self.visited[start_y + y][start_x + x] = True

    def _get_unvisited_neighbors(self, x: int, y: int) -> list[tuple[str, int, int]]:
        neighbors = []
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
        if hasattr(self.config, "seed") and self.config.seed:
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

        if not self.config.perfect:
            self._make_imperfect()

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
                    if (
                        0 <= nx < self.config.width
                        and 0 <= ny < self.config.height
                        and (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny, path + direction_char))
        return ""

    def _make_imperfect(self) -> None:
        import random

        pattern = MazeConfig.PATTERN_42
        pattern_h = len(pattern)
        pattern_w = len(pattern[0])

        start_y = self.config.height // 2 - 2
        start_x = self.config.width // 2 - 3

        def is_protected(cx: int, cy: int) -> bool:
            if (
                start_x <= cx < start_x + pattern_w
                and start_y <= cy < start_y + pattern_h
            ):
                return pattern[cy - start_y][cx - start_x] == "1"
            return False

        dead_end_values = {7, 11, 13, 14}

        # ADIM 1: Haritadaki TÜM çıkmaz sokakları (dead-ends) bul ve aç
        for y in range(self.config.height):
            for x in range(self.config.width):
                if is_protected(x, y):
                    continue

                if self.grid[y][x] in dead_end_values:
                    possible_walls = []
                    for direction, (dy, dx, bit_current, bit_next) in DIRECTIONS.items():
                        nx, ny = x + dx, y + dy

                        if (
                            0 <= nx < self.config.width
                            and 0 <= ny < self.config.height
                            and not is_protected(nx, ny)
                            and (self.grid[y][x] & bit_current) != 0
                        ):
                            possible_walls.append((nx, ny, bit_current, bit_next))

                    if possible_walls:
                        nx, ny, bit_current, bit_next = random.choice(possible_walls)
                        self.grid[y][x] -= bit_current
                        self.grid[ny][nx] -= bit_next

        # ADIM 2: Köşeler ve Merkez Garantisi (Pac-Man Ready)
        critical_points = [
            (0, 0),
            (self.config.width - 1, 0),
            (0, self.config.height - 1),
            (self.config.width - 1, self.config.height - 1),
            (self.config.width // 2, self.config.height // 2),
        ]

        for cx, cy in critical_points:
            if is_protected(cx, cy):
                continue

            while bin(self.grid[cy][cx]).count("1") > 2:
                possible_walls = []
                for direction, (dy, dx, bit_current, bit_next) in DIRECTIONS.items():
                    nx, ny = cx + dx, cy + dy

                    if (
                        0 <= nx < self.config.width
                        and 0 <= ny < self.config.height
                        and not is_protected(nx, ny)
                        and (self.grid[cy][cx] & bit_current) != 0
                    ):
                        possible_walls.append((nx, ny, bit_current, bit_next))

                if possible_walls:
                    nx, ny, bit_current, bit_next = random.choice(possible_walls)
                    self.grid[cy][cx] -= bit_current
                    self.grid[ny][nx] -= bit_next
                else:
                    break

    def save_to_file(self) -> None:
        try:
            with open(self.config.output_file, "w") as f:
                for row in self.grid:
                    hex_row = "".join(f"{cell:X}" for cell in row)
                    f.write(f"{hex_row}\n")
                f.write("\n")
                f.write(f"{self.config.entry[0]},{self.config.entry[1]}\n")
                f.write(f"{self.config.exit[0]},{self.config.exit[1]}\n")
                path = self._solve_maze()
                f.write(f"{path}\n")
        except Exception as e:
            print(f"Error writing to output file: {e}")

    def debug_print(self) -> None:
        for row in self.grid:
            print("".join(f"{cell:X}" for cell in row))
