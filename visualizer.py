"""
A-Maze-ing ASCII Visualizer Module.
Handles parsing of the hex maze file, terminal rendering, and animations.
"""

import os
import sys
import time
from typing import Any

from maze_generator import MazeGenerator
from parser import parser_config

# ANSI Color Codes for terminal UI
COLORS: dict[str, str] = {
    "reset": "\033[0m",
    "indigo": "\033[38;5;54m",
    "navy": "\033[38;5;17m",
    "khaki": "\033[38;5;143m",
    "anthracite": "\033[38;5;237m",
    "path": "\033[38;5;39m",      
    "start": "\033[48;5;118m\033[30m", # Yeşil arka plan, siyah yazı
    "end": "\033[48;5;196m\033[30m",   # Kırmızı arka plan, siyah yazı
    "pattern_42": "\033[38;5;226m"     
}

COLOR_NAMES: list[str] = ["indigo", "navy", "khaki", "anthracite"]

# Duvarları çizerken kullanılacak karakterlerin listesi
WALL_CHARS = "╋┫┣┻┳┃━┗┛┏┓╹╻╸╺"

def parse_maze_file(filepath: str) -> tuple[list[str], tuple[int, int], tuple[int, int], str]:
    """Reads the generated hexadecimal maze output file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.read().splitlines()]
    except FileNotFoundError:
        print(f"Error: Maze output file '{filepath}' not found.")
        sys.exit(1)

    hex_grid: list[str] = []
    idx: int = 0
    while idx < len(lines) and lines[idx] != "":
        hex_grid.append(lines[idx])
        idx += 1

    idx += 1 

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


def build_ascii_grid(hex_grid: list[str]) -> list[list[str]]:
    """Converts the hexadecimal grid into an ASCII box-drawing matrix with smart intersections."""
    height: int = len(hex_grid)
    width: int = len(hex_grid[0]) if height > 0 else 0

    grid_h: int = height * 2 + 1
    grid_w: int = width * 4 + 1

    ascii_grid: list[list[str]] = [[' ' for _ in range(grid_w)] for _ in range(grid_h)]

    # Önce sadece yatay ve dikey duvarları yerleştir
    for y in range(height):
        for x in range(width):
            val: int = int(hex_grid[y][x], 16)

            if val & 1:  # Kuzey
                for i in range(1, 4): ascii_grid[y * 2][x * 4 + i] = '━'
            if val & 2:  # Doğu
                ascii_grid[y * 2 + 1][x * 4 + 4] = '┃'
            if val & 4:  # Güney
                for i in range(1, 4): ascii_grid[y * 2 + 2][x * 4 + i] = '━'
            if val & 8:  # Batı
                ascii_grid[y * 2 + 1][x * 4] = '┃'
            if val == 15:  # 42 deseni hücresi
                for i in range(1, 4):
                    ascii_grid[y * 2 + 1][x * 4 + i] = '▒'

    # Akıllı Köşe (Smart Intersection) Algoritması
    # Duvarların geliş yönüne göre en doğru köşe bağlantı parçasını seçer
    for y in range(height + 1):
        for x in range(width + 1):
            grid_y, grid_x = y * 2, x * 4
            
            up = (grid_y > 0 and ascii_grid[grid_y - 1][grid_x] == '┃')
            down = (grid_y < grid_h - 1 and ascii_grid[grid_y + 1][grid_x] == '┃')
            left = (grid_x > 0 and ascii_grid[grid_y][grid_x - 1] == '━')
            right = (grid_x < grid_w - 1 and ascii_grid[grid_y][grid_x + 1] == '━')
            
            char = ' '
            if up and down and left and right: char = '╋'
            elif up and down and left: char = '┫'
            elif up and down and right: char = '┣'
            elif left and right and up: char = '┻'
            elif left and right and down: char = '┳'
            elif up and down: char = '┃'
            elif left and right: char = '━'
            elif up and right: char = '┗'
            elif up and left: char = '┛'
            elif down and right: char = '┏'
            elif down and left: char = '┓'
            elif up: char = '╹'
            elif down: char = '╻'
            elif left: char = '╸'
            elif right: char = '╺'
            
            ascii_grid[grid_y][grid_x] = char

    return ascii_grid


def get_rendered_lines(ascii_grid: list[list[str]],
                       entry: tuple[int, int],
                       exit_pos: tuple[int, int],
                       path: str,
                       show_path: bool,
                       wall_color: str) -> list[str]:
    """Applies colors and path arrows, returning the grid as a list of strings."""
    grid_copy: list[list[str]] = [row[:] for row in ascii_grid]

    if show_path:
        cx, cy = entry
        for move in path:
            if move == 'N':
                char, nx, ny = '↑', cx, cy - 1
            elif move == 'S':
                char, nx, ny = '↓', cx, cy + 1
            elif move == 'E':
                char, nx, ny = '→', cx + 1, cy
            elif move == 'W':
                char, nx, ny = '←', cx - 1, cy

            grid_copy[cy * 2 + 1][cx * 4 + 2] = char
            cx, cy = nx, ny

    color_code: str = COLORS[wall_color]
    reset: str = COLORS["reset"]
    
    lines_out: list[str] = []

    for y, row in enumerate(grid_copy):
        row_str: str = ""
        for x, char in enumerate(row):
            maze_y, maze_x = (y - 1) // 2, (x - 2) // 4

            if char in WALL_CHARS:
                row_str += f"{color_code}{char}{reset}"
            elif char == '▒':
                row_str += f"{COLORS['pattern_42']}▒{reset}"
            elif char in ('↑', '↓', '→', '←'):
                row_str += f"\033[1m{COLORS['path']}{char}{reset}"
            elif maze_x == entry[0] and maze_y == entry[1] and (y % 2 != 0) and (x % 4 == 2):
                 row_str += f"{COLORS['start']} S {reset}"
            elif maze_x == exit_pos[0] and maze_y == exit_pos[1] and (y % 2 != 0) and (x % 4 == 2):
                 row_str += f"{COLORS['end']} E {reset}"
            else:
                row_str += char
        lines_out.append(row_str)
        
    return lines_out


def draw_screen(lines: list[str], menu_text: str) -> None:
    """Draws the screen without flickering using ANSI cursor repositioning."""
    sys.stdout.write('\033[H' + '\n'.join(lines) + '\n' + menu_text)
    sys.stdout.flush()


def start_ui(output_file: str, generator: Any) -> None:
    """Main interactive loop with animations."""
    show_path: bool = False
    color_idx: int = 0

    if os.name == 'nt':
        os.system('')
    
    os.system('cls' if os.name == 'nt' else 'clear')

    menu_text = (
        "\n=== A-Maze-ing ===\n"
        "1. Re-generate a new maze\n"
        "2. Show/Hide the shortest path\n"
        "3. Change wall colours\n"
        "4. Quit\n"
        "Choice? (1-4): "
    )

    while True:
        hex_grid, entry, exit_pos, full_path = parse_maze_file(output_file)
        ascii_grid = build_ascii_grid(hex_grid)

        lines = get_rendered_lines(ascii_grid, entry, exit_pos, full_path if show_path else "", show_path, COLOR_NAMES[color_idx])
        draw_screen(lines, menu_text)

        try:
            choice = input().strip()
        except KeyboardInterrupt:
            print("\nExiting gracefully...")
            break

        if choice == '1':
            config = parser_config()
            new_gen = MazeGenerator(config)
            new_gen.generate()
            new_gen.save_to_file()
            
            hex_grid, entry, exit_pos, full_path = parse_maze_file(config.output_file)
            ascii_grid = build_ascii_grid(hex_grid)
            show_path = False
            
            os.system('cls' if os.name == 'nt' else 'clear')
            for i in range(1, len(ascii_grid) + 1):
                partial_grid = ascii_grid[:i]
                lines = get_rendered_lines(partial_grid, entry, exit_pos, "", False, COLOR_NAMES[color_idx])
                sys.stdout.write('\033[H' + '\n'.join(lines) + '\n')
                sys.stdout.flush()
                time.sleep(0.015) 

        elif choice == '2':
            show_path = not show_path
            
            if show_path:
                current_path = ""
                for move in full_path:
                    current_path += move
                    lines = get_rendered_lines(ascii_grid, entry, exit_pos, current_path, True, COLOR_NAMES[color_idx])
                    draw_screen(lines, menu_text)
                    time.sleep(0.02) 

        elif choice == '3':
            color_idx = (color_idx + 1) % len(COLOR_NAMES)

        elif choice == '4':
            os.system('cls' if os.name == 'nt' else 'clear')
            break