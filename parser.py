import sys

from maze_config import MazeConfig


def parse_int(line: str) -> int:
    value: int = 0
    try:
        value = int(line)
    except ValueError:
        print("ERROR: Invalid integer value")
        sys.exit(1)
    return value


def parse_tuple(val: str) -> tuple[int, int]:
    tuple_prts: list[str] = val.split(",")

    if len(tuple_prts) != 2:
        print("ERROR: Invalid tuple format")
        sys.exit(1)

    try:
        value = (int(tuple_prts[0]), int(tuple_prts[1]))
    except ValueError:
        print("ERROR: Invalid integer value")
        sys.exit(1)

    return value


def parser_config() -> MazeConfig:
    if len(sys.argv) != 2:
        print("Error: Usage: python3 a_maze_ing.py <config_file>")
        sys.exit(1)

    file_name: str = sys.argv[1]

    width: int = 0
    height: int = 0
    entry: tuple[int, int] = (-1, -1)
    exit: tuple[int, int] = (-1, -1)
    output_file: str = ""
    is_perfect: bool | None = None
    seed: int | None = None

    try:
        with open(file_name, "r") as config_file:
            output: list[str] = config_file.readlines()
            for line in output:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                out: list[str] = line.split("=", 1)
                if len(out) != 2:
                    print(f"ERROR: Invalid line format -> {line}")
                    sys.exit(1)
                key = out[0].strip().upper()
                val = out[1].strip()
                if key == "WIDTH":
                    width = parse_int(val)
                elif key == "HEIGHT":
                    height = parse_int(val)
                elif key == "ENTRY":
                    entry = parse_tuple(val)
                elif key == "EXIT":
                    exit = parse_tuple(val)
                elif key == "OUTPUT_FILE":
                    output_file = val
                elif key == "PERFECT":
                    val = val.upper()
                    if val == "TRUE":
                        is_perfect = True
                    elif val == "FALSE":
                        is_perfect = False
                    else:
                        print("ERROR: Invalid boolean parameter for PERFECT")
                        sys.exit(1)
                elif key == "SEED":
                    seed = parse_int(val)
                else:
                    raise ValueError(
                        f"ERROR: Unknown configuration key: '{key}'"
                    )

    except ValueError as e:
        print(f"{e}")
        sys.exit(1)
    if (
        width <= 0
        or height <= 0
        or not output_file.strip()
        or entry == (-1, -1)
        or exit == (-1, -1)
        or is_perfect is None
    ):
        print("ERROR: Missing mandatory configuration keys")
        sys.exit(1)
    return MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit,
        output_file=output_file,
        is_perfect=is_perfect,
        seed=seed,
    )


def is_valid_maze(maze: MazeConfig) -> bool:
    pattern_w: int = len(MazeConfig.PATTERN_42[0])
    pattern_h: int = len(MazeConfig.PATTERN_42)

    if maze.width < pattern_w + 2 or maze.height < pattern_h + 2:
        print("ERROR: Maze is too small for display 42 pattern.")

    if not (
        0 < maze.width
        and 0 < maze.height
        and 0 <= maze.entry[0] < maze.width
        and 0 <= maze.entry[1] < maze.height
        and 0 <= maze.exit[0] < maze.width
        and 0 <= maze.exit[1] < maze.height
        and maze.entry != maze.exit
    ):
        print("ERROR: Invalid entry/exit coordinates or out of bounds.")
        return False

    if maze.width >= pattern_w + 2 and maze.height >= pattern_h + 2:
        start_x: int = maze.width // 2 - (pattern_w // 2)
        start_y: int = maze.height // 2 - (pattern_h // 2)
        for px, py in (maze.entry, maze.exit):
            if (
                start_x <= px < start_x + pattern_w
                and start_y <= py < start_y + pattern_h
                and MazeConfig.PATTERN_42[py - start_y][px - start_x] == "1"
            ):
                print("Error: ENTRY or EXIT coordinate on 42 pattern wall.")
                return False

    return True
