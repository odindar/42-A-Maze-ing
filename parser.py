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


def parse_tuple(line: str) -> tuple[int, int]:
    parts: list[str] = line.split("=")
    value: tuple[int, int] = (0, 0)
    if len(parts) != 2:
        print("ERROR: Invalid tuple format")
        sys.exit(1)
    tuple_prts: list[str] = parts[1].split(",")
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
    is_perfect: bool = False
    seed: int | None = None

    try:
        with open(file_name, "r") as config_file:
            output = config_file.readlines()
            for line in output:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue

                out = line.split("=", 1)
                if len(out) != 2:
                    print(f"Error: Invalid line format -> {line}")
                    sys.exit(1)
                key = out[0].strip().upper()
                val = out[1].strip()
                if key == "WIDTH":
                    width = parse_int(val)
                elif key == "HEIGHT":
                    height = parse_int(val)
                elif key == "ENTRY":
                    entry = parse_tuple(f"{key}={val}")
                elif key == "EXIT":
                    exit = parse_tuple(f"{key}={val}")
                elif key == "OUTPUT_FILE":
                    output_file = val
                elif key == "PERFECT":
                    if val == "True":
                        is_perfect = True
                    elif val == "False":
                        is_perfect = False
                    else:
                        print(f"Error: Invalid boolean parameter for PERFECT -> {val}")
                        sys.exit(1)
                elif key == "SEED":
                    seed = parse_int(val)
                else:
                    raise ValueError("Config Error")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    if (
        width == 0
        or height == 0
        or output_file == ""
        or entry == (-1, -1)
        or exit == (-1, -1)
        or is_perfect is None
    ):
        print("Error: Missing mandatory configuration keys")
        sys.exit(1)
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
        print("WARNING: Maze is too small for display 42 pattern.")

    if not (
        0 < maze.width
        and 0 < maze.height
        and 0 <= maze.entry[0] < maze.width
        and 0 <= maze.entry[1] < maze.height
        and 0 <= maze.exit[0] < maze.width
        and 0 <= maze.exit[1] < maze.height
        and maze.entry != maze.exit
    ):
        print("Error: Invalid entry/exit coordinates or out of bounds.")
        return False
    pattern = [
        "1000111",
        "1000001",
        "1110111",
        "0010100",
        "0010111",
    ]
    if maze.width >= 9 and maze.height >= 7:
        start_x = maze.width // 2 - 3
        start_y = maze.height // 2 - 2
        for px, py in (maze.entry, maze.exit):
            if (
                start_x <= px < start_x + 7
                and start_y <= py < start_y + 5
                and pattern[py - start_y][px - start_x] == "1"
            ):
                    print("Error: ENTRY or EXIT coordinate on 42 pattern wall.")
                    return False

    return True
