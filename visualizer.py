"""
A-Maze-ing ASCII Visualizer Module.
Handles parsing of the hex maze file, terminal rendering, and animations.
"""

import os
import sys
import time
from typing import Any, ClassVar

from maze_generator import MazeGenerator


class MazeVisualizer:
    COLORS: ClassVar[dict[str, str]] = {
        "reset": "\033[0m",
        "indigo": "\033[38;2;251;44;54m",
        "navy": "\033[38;5;17m",
        "khaki": "\033[38;5;143m",
        "anthracite": "\033[38;5;237m",
        "path": "\033[38;5;39m",
        "start": "\033[48;5;118m\033[30m",
        "end": "\033[48;5;196m\033[30m",
        "pattern_42": "\033[36;8;43m",
    }

    COLOR_NAMES: ClassVar[list[str]] = ["indigo", "navy", "khaki", "anthracite"]

    WALL_CHARS: str = "╋┫┣┻┳┃━┗┛┏┓╹╻╸╺"

    def __init__(self, output_file: str, generator: Any):
        self.output_file = output_file
        self.generator = generator

    def parse_maze_file(
        self, filepath: str
    ) -> tuple[list[str], tuple[int, int], tuple[int, int], str]:
        """Reads the generated hexadecimal maze output file."""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().strip()
        except FileNotFoundError:
            print(f"Error: Maze output file '{filepath}' not found.")
            sys.exit(1)

        parts = content.replace("\r", "").split("\n\n")

        hex_grid = parts[0].splitlines()
        footer_lines = parts[1].splitlines()

        try:
            e_x, e_y = map(int, footer_lines[0].split("#")[0].strip().split(","))
            ex_x, ex_y = map(int, footer_lines[1].split("#")[0].strip().split(","))
            path = footer_lines[2] if len(footer_lines) > 2 else ""
        except (IndexError, ValueError) as e:
            print(f"Error parsing maze footer data: {e}")
            sys.exit(1)

        return hex_grid, (e_x, e_y), (ex_x, ex_y), path

    def build_ascii_grid(self, hex_grid: list[str]) -> list[list[str]]:
        """Converts the hexadecimal grid into an ASCII box-drawing matrix."""
        height: int = len(hex_grid)
        width: int = len(hex_grid[0]) if height > 0 else 0

        grid_h: int = height * 2 + 1
        grid_w: int = width * 4 + 1

        ascii_grid = [[" " for _ in range(grid_w)] for _ in range(grid_h)]

        for y in range(height + 1):
            for x in range(width + 1):
                ascii_grid[y * 2][x * 4] = "+"

        for y in range(height):
            for x in range(width):
                val: int = int(hex_grid[y][x], 16)

                if val & 1:
                    for i in range(1, 4):
                        ascii_grid[y * 2][x * 4 + i] = "-"
                if val & 2:
                    ascii_grid[y * 2 + 1][x * 4 + 4] = "|"
                if val & 4:
                    for i in range(1, 4):
                        ascii_grid[y * 2 + 2][x * 4 + i] = "-"
                if val & 8:
                    ascii_grid[y * 2 + 1][x * 4] = "|"
                if val == 15:
                    for i in range(1, 4):
                        ascii_grid[y * 2 + 1][x * 4 + i] = "#"

        final_grid = [[" " for _ in range(grid_w)] for _ in range(grid_h)]
        for y in range(grid_h):
            for x in range(grid_w):
                char = ascii_grid[y][x]
                if char == "-":
                    final_grid[y][x] = "━"
                elif char == "|":
                    final_grid[y][x] = "┃"
                elif char == "#":
                    final_grid[y][x] = "▓"
                elif char == "+":
                    up = y > 0 and ascii_grid[y - 1][x] == "|"
                    down = y < grid_h - 1 and ascii_grid[y + 1][x] == "|"
                    left = x > 0 and ascii_grid[y][x - 1] == "-"
                    right = x < grid_w - 1 and ascii_grid[y][x + 1] == "-"

                    if up and down and left and right:
                        final_grid[y][x] = "╋"
                    elif up and down and left:
                        final_grid[y][x] = "┫"
                    elif up and down and right:
                        final_grid[y][x] = "┣"
                    elif left and right and up:
                        final_grid[y][x] = "┻"
                    elif left and right and down:
                        final_grid[y][x] = "┳"
                    elif up and down:
                        final_grid[y][x] = "┃"
                    elif left and right:
                        final_grid[y][x] = "━"
                    elif up and right:
                        final_grid[y][x] = "┗"
                    elif up and left:
                        final_grid[y][x] = "┛"
                    elif down and right:
                        final_grid[y][x] = "┏"
                    elif down and left:
                        final_grid[y][x] = "┓"
                    elif up:
                        final_grid[y][x] = "╹"
                    elif down:
                        final_grid[y][x] = "╻"
                    elif left:
                        final_grid[y][x] = "╸"
                    elif right:
                        final_grid[y][x] = "╺"
                    else:
                        final_grid[y][x] = " "
                else:
                    final_grid[y][x] = " "

        return final_grid

    def get_rendered_lines(
        self,
        ascii_grid: list[list[str]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        path: str,
        show_path: bool,
        wall_color: str,
    ) -> list[str]:
        """Applies colors and path arrows, returning grid as a list of strings."""
        grid_copy = [row[:] for row in ascii_grid]

        cx_s, cy_s = entry
        cx_e, cy_e = exit_pos

        if cy_s * 2 + 1 < len(grid_copy):
            grid_copy[cy_s * 2 + 1][cx_s * 4 + 2] = "S"

        if cy_e * 2 + 1 < len(grid_copy):
            grid_copy[cy_e * 2 + 1][cx_e * 4 + 2] = "E"

        if show_path:
            cx, cy = entry
            for move in path:
                char, nx, ny = "", cx, cy
                if move == "N":
                    char, nx, ny = "↑", cx, cy - 1
                elif move == "S":
                    char, nx, ny = "↓", cx, cy + 1
                elif move == "E":
                    char, nx, ny = "→", cx + 1, cy
                elif move == "W":
                    char, nx, ny = "←", cx - 1, cy

                if cy * 2 + 1 < len(grid_copy) and grid_copy[cy * 2 + 1][
                    cx * 4 + 2
                ] not in ("S", "E"):
                    grid_copy[cy * 2 + 1][cx * 4 + 2] = char
                cx, cy = nx, ny

        color_code: str = self.COLORS[wall_color]
        reset: str = self.COLORS["reset"]

        lines_out: list[str] = []

        for row in grid_copy:
            row_str: str = ""
            for char in row:
                if char == "S":
                    row_str += f"{self.COLORS['start']}S{reset}"
                elif char == "E":
                    row_str += f"{self.COLORS['end']}E{reset}"
                elif char in self.WALL_CHARS:
                    row_str += f"{color_code}{char}{reset}"
                elif char == "▓":
                    row_str += f"{self.COLORS['pattern_42']}▓{reset}"
                elif char in ("↑", "↓", "→", "←"):
                    row_str += f"\033[1m{self.COLORS['path']}{char}{reset}"
                else:
                    row_str += char
            lines_out.append(row_str)

        return lines_out

    def draw_screen(self, lines: list[str], menu_text: str) -> None:
        """Draws the screen cleanly using ANSI codes to prevent artifacts."""
        sys.stdout.write("\033[H" + "\n".join(lines) + "\n" + menu_text + "\033[J")
        sys.stdout.flush()

    def animate_maze(
        self,
        ascii_grid: list[list[str]],
        entry: tuple[int, int],
        exit_pos: tuple[int, int],
        color_name: str,
    ) -> None:
        """Animates the maze generation line by line."""
        os.system("cls" if os.name == "nt" else "clear")
        for i in range(1, len(ascii_grid) + 1):
            partial_grid = ascii_grid[:i]
            lines = self.get_rendered_lines(
                partial_grid, entry, exit_pos, "", False, color_name
            )
            print("\033[H" + "\n".join(lines) + "\n\033[J", end="", flush=True)
            time.sleep(0.04)

    def run_ui(self) -> None:
        """Main interactive loop with animations."""
        show_path: bool = False
        color_idx: int = 0

        if os.name == "nt":
            os.system("")

        hex_grid, entry, exit_pos, full_path = self.parse_maze_file(self.output_file)
        ascii_grid = self.build_ascii_grid(hex_grid)

        self.animate_maze(ascii_grid, entry, exit_pos, self.COLOR_NAMES[color_idx])

        menu_text = (
            "\n=== A-Maze-ing ===\n"
            "1. Re-generate a new maze\n"
            "2. Show/Hide the shortest path\n"
            "3. Change wall colours\n"
            "4. Quit\n"
            "Choice? (1-4): "
        )

        while True:
            lines = self.get_rendered_lines(
                ascii_grid,
                entry,
                exit_pos,
                full_path if show_path else "",
                show_path,
                self.COLOR_NAMES[color_idx],
            )
            self.draw_screen(lines, menu_text)

            try:
                choice = input().strip()
            except KeyboardInterrupt:
                print("\nExiting gracefully...")
                break

            os.system("cls" if os.name == "nt" else "clear")

            if choice == "1":
                new_gen = MazeGenerator(self.generator.config)
                new_gen.generate()
                new_gen.save_to_file()

                hex_grid, entry, exit_pos, full_path = self.parse_maze_file(
                    self.generator.config.output_file
                )
                ascii_grid = self.build_ascii_grid(hex_grid)
                show_path = False

                self.animate_maze(
                    ascii_grid, entry, exit_pos, self.COLOR_NAMES[color_idx]
                )

            elif choice == "2":
                show_path = not show_path

                if show_path:
                    current_path = ""
                    for move in full_path:
                        current_path += move
                        lines = self.get_rendered_lines(
                            ascii_grid,
                            entry,
                            exit_pos,
                            current_path,
                            True,
                            self.COLOR_NAMES[color_idx],
                        )
                        self.draw_screen(lines, menu_text)
                        time.sleep(0.05)

            elif choice == "3":
                color_idx = (color_idx + 1) % len(self.COLOR_NAMES)

            elif choice == "4":
                break
