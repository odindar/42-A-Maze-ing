#!/usr/bin/env python3

import sys

from maze_config import MazeConfig
from maze_generator import MazeGenerator
from parser import MazeParser
from visualizer import MazeVisualizer

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    try:
        parser: MazeParser = MazeParser(sys.argv[1])
        config: MazeConfig = parser.parse_config()
    except (ValueError, FileNotFoundError) as e:
        print(f"{e}")
        sys.exit(1)

    if parser.is_valid_maze(config):
        generator: MazeGenerator = MazeGenerator(config)
        generator.generate()
        try:
            generator.save_to_file()
        except RuntimeError as e:
            print(f"{e}")
            sys.exit(1)
        try:
            visualizer = MazeVisualizer(config.output_file, generator)
            visualizer.run_ui()
        except (ValueError, FileNotFoundError) as e:
            print(f"{e}")
            sys.exit(1)
    else:
        print("ERROR: Map is not valid.")
        sys.exit(1)
