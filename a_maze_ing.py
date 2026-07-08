#!/usr/bin/env python3

from parser import parser_config, is_valid_maze
from maze_generator import MazeGenerator

def main() -> None:
    config = parser_config()
    if is_valid_maze(config):
        generator = MazeGenerator(config)
        generator.generate()
        generator.save_to_file()
        generator.debug_print()
    else:
        print("Error")
        return

if __name__ == "__main__":
    main()
