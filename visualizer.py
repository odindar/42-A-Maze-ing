"""
A-Maze-ing ASCII Visualizer Module.
Handles parsing of the hex maze file and terminal rendering.
"""

import os
import sys
from typing import List, Tuple, Dict, Any

# ANSI Color Codes for terminal UI
COLORS: Dict[str, str] = {
    "reset": "\033[0m",
    "indigo": "\033[38;5;54m",
    "navy": "\033[38;5;17m",
    "khaki": "\033[38;5;143m",
    "anthracite": "\033[38;5;237m",
    "path": "\033[48;5;39m",
    "start": "\033[48;5;118m",
    "end": "\033[48;5;196m",
    "pattern_42": "\033[48;5;226m"
}

COLOR_NAMES: List[str] = ["indigo", "navy", "khaki", "anthracite"]

def parse_maze_file(filepath: str) -> Tuple[List[str], Tuple[int, int], Tuple[int, int], str]:
    """Reads the generated hexadecimal maze output file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.read().splitlines()]
    except FileNotFoundError:
        print(f"Error: Maze output file '{filepath}' not found.")
        sys.exit(1)

    hex_grid: List[str] = []
    idx: int = 0
    while idx < len(lines) and lines[idx] != "":
        hex_grid.append(lines[idx])
        idx += 1

    idx += 1 # Skip empty line

    try:
        entry_str = lines[idx].split('#')[0].strip()
        e_x, e_y = map(int, entry_str.split(','))
        idx += 1

        exit_str = lines[idx].split('#')[0].strip()
        ex_x, ex_y = map(int, exit_str.split(','))
        idx += 1

        path = lines[idx]
    except (IndexError, ValueError) as e:
        print(f"Error parsing maze footer data: {e}")
        sys.exit(1)

    return hex_grid, (e_x, e_y), (ex_x, ex_y), path


def build_ascii_grid(hex_grid: List[str]) -> List[List[str]]:
    """Converts the hexadecimal grid into an ASCII character matrix."""
    height: int = len(hex_grid)
    width: int = len(hex_grid[0]) if height > 0 else 0

    grid_h: int = height * 2 + 1
    grid_w: int = width * 4 + 1
    
    ascii_grid: List[List[str]] = [[' ' for _ in range(grid_w)] for _ in range(grid_h)]

    for y in range(height + 1):
        for x in range(width + 1):
            ascii_grid[y * 2][x * 4] = '+'

    for y in range(height):
        for x in range(width):
            val: int = int(hex_grid[y][x], 16)
            
            if val & 1:
                for i in range(1, 4): ascii_grid[y * 2][x * 4 + i] = '-'
            if val & 2:
                ascii_grid[y * 2 + 1][x * 4 + 4] = '|'
            if val & 4:
                for i in range(1, 4): ascii_grid[y * 2 + 2][x * 4 + i] = '-'
            if val & 8:
                ascii_grid[y * 2 + 1][x * 4] = '|'
            if val == 15:
                for i in range(1, 4):
                    ascii_grid[y * 2 + 1][x * 4 + i] = '#'

    return ascii_grid


def render_maze(ascii_grid: List[List[str]],
                entry: Tuple[int, int],
                exit_pos: Tuple[int, int],
                path: str,
                show_path: bool,
                wall_color: str) -> None:
    """Prints the ASCII grid to the terminal with applied colors and path."""
    grid_copy: List[List[str]] = [row[:] for row in ascii_grid]
    
    if show_path:
        cx, cy = entry
        grid_copy[cy * 2 + 1][cx * 4 + 2] = '.'
        for move in path:
            if move == 'N': cy -= 1
            elif move == 'S': cy += 1
            elif move == 'E': cx += 1
            elif move == 'W': cx -= 1
            grid_copy[cy * 2 + 1][cx * 4 + 2] = '.'

    color_code: str = COLORS[wall_color]
    reset: str = COLORS["reset"]
    
    for y, row in enumerate(grid_copy):
        row_str: str = ""
        for x, char in enumerate(row):
            maze_y, maze_x = (y - 1) // 2, (x - 2) // 4
            
            if char in ('+', '-', '|'):
                row_str += f"{color_code}{char}{reset}"
            elif char == '#':
                row_str += f"{COLORS['pattern_42']} {reset}"
            elif char == '.':
                row_str += f"{COLORS['path']} {reset}"
            elif maze_x == entry[0] and maze_y == entry[1] and (y % 2 != 0) and (x % 4 == 2):
                 row_str += f"{COLORS['start']}S{reset}"
            elif maze_x == exit_pos[0] and maze_y == exit_pos[1] and (y % 2 != 0) and (x % 4 == 2):
                 row_str += f"{COLORS['end']}E{reset}"
            else:
                row_str += char
        print(row_str)


def start_ui(output_file: str, generator: Any) -> None:
    """Main interactive loop for the visualizer."""
    show_path: bool = False
    color_idx: int = 0
    
    while True:
        hex_grid, entry, exit_pos, path = parse_maze_file(output_file)
        ascii_grid = build_ascii_grid(hex_grid)
        
        os.system('cls' if os.name == 'nt' else 'clear')
        render_maze(ascii_grid, entry, exit_pos, path, show_path, COLOR_NAMES[color_idx])
        
        print("\n=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show/Hide the shortest path")
        print("3. Change wall colours")
        print("4. Quit")
        
        try:
            choice = input("Choice? (1-4): ").strip()
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            break

        if choice == '1':
            generator.generate()
            generator.save_to_file()
        elif choice == '2':
            show_path = not show_path
        elif choice == '3':
            color_idx = (color_idx + 1) % len(COLOR_NAMES)
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please select 1-4.")