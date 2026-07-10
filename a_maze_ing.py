#!/usr/bin/env python3

from parser import parser_config, is_valid_maze
from maze_generator import MazeGenerator
from visualizer import start_ui 

def main() -> None:
    config = parser_config()
    
    if is_valid_maze(config):
        generator = MazeGenerator(config)
        generator.generate()
        generator.save_to_file()
        
        output_filepath = config.output_file 
        
        start_ui(output_filepath, generator)
    else:
        print("Error")
        return

if __name__ == "__main__":
    main()