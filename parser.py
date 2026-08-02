from maze_config import MazeConfig


class MazeParser:
    def __init__(self, file_name: str):
        self.file_name = file_name

    def _parse_int(self, line: str) -> int:
        value: int = 0
        try:
            value = int(line)
        except ValueError:
            raise ValueError("ERROR: Invalid integer value")
        return value

    def _parse_tuple(self, val: str) -> tuple[int, int]:
        tuple_prts: list[str] = val.split(",")

        if len(tuple_prts) != 2:
            raise ValueError("ERROR: Invalid tuple format")

        try:
            value = (int(tuple_prts[0]), int(tuple_prts[1]))
        except ValueError:
            raise ValueError("ERROR: Invalid integer value")

        return value

    def parse_config(self) -> MazeConfig:
        width: int = 0
        height: int = 0
        entry: tuple[int, int] = (-1, -1)
        exit: tuple[int, int] = (-1, -1)
        output_file: str = ""
        is_perfect: bool | None = None
        seed: int | None = None

        seen_keys: set[str] = set()

        try:
            with open(self.file_name, "r") as config_file:
                output: list[str] = config_file.readlines()
                for line in output:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue

                    out: list[str] = line.split("=", 1)
                    if len(out) != 2:
                        raise ValueError("ERROR: Invalid line format")

                    key = out[0].strip().upper()
                    val = out[1].strip()

                    if key in seen_keys:
                        raise ValueError("ERROR: Duplicate configuration key")

                    seen_keys.add(key)

                    if key == "WIDTH":
                        width = self._parse_int(val)
                    elif key == "HEIGHT":
                        height = self._parse_int(val)
                    elif key == "ENTRY":
                        entry = self._parse_tuple(val)
                    elif key == "EXIT":
                        exit = self._parse_tuple(val)
                    elif key == "OUTPUT_FILE":
                        output_file = val
                    elif key == "PERFECT":
                        val = val.upper()
                        if val == "TRUE":
                            is_perfect = True
                        elif val == "FALSE":
                            is_perfect = False
                        else:
                            raise ValueError(
                                "ERROR: Invalid boolean parameter for PERFECT"
                            )
                    elif key == "SEED":
                        seed = self._parse_int(val)
                    else:
                        raise ValueError("ERROR: Unknown configuration key")

        except FileNotFoundError:
            raise FileNotFoundError(
                f"ERROR: Configuration file '{self.file_name}' not found."
            )

        if (
            width <= 0
            or height <= 0
            or not output_file.strip()
            or entry == (-1, -1)
            or exit == (-1, -1)
            or is_perfect is None
        ):
            raise ValueError("ERROR: Missing mandatory configuration keys")

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit=exit,
            output_file=output_file,
            is_perfect=is_perfect,
            seed=seed,
        )

    def is_valid_maze(self, maze: MazeConfig) -> bool:
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
            strt_x: int = maze.width // 2 - (pattern_w // 2)
            strt_y: int = maze.height // 2 - (pattern_h // 2)
            for px, py in (maze.entry, maze.exit):
                if (
                    strt_x <= px < strt_x + pattern_w
                    and strt_y <= py < strt_y + pattern_h
                    and MazeConfig.PATTERN_42[py - strt_y][px - strt_x] == "1"
                ):
                    print("ERROR: ENTRY/EXIT coordinate on 42 pattern wall.")
                    return False

        return True
