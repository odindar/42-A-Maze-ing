#!/usr/bin/env python3


import sys

from maze_config import MazeConfig
from maze_generator import MazeGenerator
from parser import is_valid_maze, parser_config
from visualizer import start_ui

if __name__ == "__main__":
    config: MazeConfig = parser_config()

    if is_valid_maze(config):
        generator: MazeGenerator = MazeGenerator(config)
        generator.generate()
        generator.save_to_file()
        start_ui(config.output_file, generator)
    else:
        print("ERROR: Map is not valid.")
        sys.exit(1)
