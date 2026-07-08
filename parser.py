#!/usr/bin/env python3


from typing import Tuple

from maze_config import MazeConfig


def parse_int(line: str) -> int:
    parts: list[str] = line.split("=")
    value: int = 0
    if len(parts) == 2:
        try:
            value = int(parts[1])
        except Exception as e:
            print(f"Error: {e}")
    return value


def parse_tuple(line: str) -> Tuple[int, int]:
    parts: list[str] = line.split("=")
    value: Tuple[int, int] = (0, 0)
    if len(parts) == 2:
        tuple_prts: list[str] = parts[1].split(",")
        if len(tuple_prts) == 2:
            try:
                value = (int(tuple_prts[0]), int(tuple_prts[1]))
            except Exception as e:
                print(f"Error: {e}")
    return value


def parser_config() -> MazeConfig:
    width: int = 0
    height: int = 0
    entry: Tuple[int, int] = (0, 0)
    exit: Tuple[int, int] = (0, 0)
    output_file: str = ""
    is_perfect: bool = False
    seed: int | None = None
    try:
        with open("config.txt", "r") as config_file:
            output = config_file.readlines()
            for out in output:
                out = out.strip()
                if out.startswith("#"):
                    continue
                elif out.startswith("WIDTH"):
                    width = parse_int(out)
                elif out.startswith("HEIGHT"):
                    height = parse_int(out)
                elif out.startswith("ENTRY"):
                    entry = parse_tuple(out)
                elif out.startswith("EXIT"):
                    exit = parse_tuple(out)
                elif out.startswith("OUTPUT_FILE"):
                    output_file = out.split("=")[1]
                elif out.startswith("PERFECT"):
                    is_perfect = out.split("=")[1] == "True"
                elif out.startswith("SEED"):
                    seed = parse_int(out)

    except Exception as e:
        print(f"Error: {e}")
    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        perfect=is_perfect,
        seed=seed,
    )


def is_valid_maze(maze: MazeConfig) -> bool:
    if maze.width < 7 or maze.height < 5:
        print("Warning: Maze is too small for display 42 pattern.")
    return (
        0 < maze.width and 0 < maze.height and
        0 <= maze.entry[0] < maze.width and
        0 <= maze.entry[1] < maze.height and
        0 <= maze.exit[0] < maze.width and
        0 <= maze.exit[1] < maze.height and
        maze.entry != maze.exit
    )
