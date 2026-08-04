*This project has been created as part of the 42 curriculum by odindar, iergin.*

# A-Maze-ing

## Description

A-Maze-ing is a Python project that generates random mazes from a configuration file. The program supports both perfect and imperfect mazes, saves the generated maze to an output file, computes the solution path, and displays the maze using a graphical visualizer.

## Instructions

### Requirements

- Python 3

### Run

```bash
python3 a_maze_ing.py <config_file>
```

Example:

```bash
python3 a_maze_ing.py config.txt
```

The program will:

- Parse the configuration file.
- Validate the configuration.
- Generate the maze.
- Save the maze into the output file.
- Find the solution path.
- Open the graphical visualizer.

---

## Configuration File Format

Example:

```text
WIDTH=20
HEIGHT=20
ENTRY=0,0
EXIT=19,19
OUTPUT_FILE=maze.txt
PERFECT=TRUE
SEED=42
```

Parameters:

- `WIDTH` : Maze width.
- `HEIGHT` : Maze height.
- `ENTRY` : Starting cell.
- `EXIT` : Exit cell.
- `OUTPUT_FILE` : Output file name.
- `PERFECT` : TRUE or FALSE.
- `SEED` : Optional random seed.

---

## Maze Generation Algorithm

The maze is generated using the **Iterative Recursive Backtracking (Depth-First Search)** algorithm.

The algorithm starts from the entry point, randomly visits unvisited neighboring cells, removes the walls between them, and backtracks when no unvisited neighbors remain.

If `PERFECT=FALSE`, additional walls are removed after generation to create loops, producing an imperfect maze.

### Why this algorithm?

We chose this algorithm because it is simple to implement, fast, and generates perfect mazes with a unique path between cells. It was also easy to extend for imperfect maze generation.

---

## Maze Solving

The solution path is found using the **Breadth-First Search (BFS)** algorithm.

---

## Reusable Code

The parser and maze generation modules are independent from the graphical interface and can be reused in other Python projects.

Example:

```python
from parser import MazeParser
from maze_generator import MazeGenerator

parser = MazeParser("config.txt")
config = parser.parse_config()

generator = MazeGenerator(config)
generator.generate()
generator.save_to_file()
```

The generated maze is stored in `generator.grid`, and the output can also be written to a file using `save_to_file()`.

## Resources

Documentation used:

- Python Documentation
- Python dataclasses documentation
- Python random module documentation
- Python collections.deque documentation

### AI Usage

- understand some Python features,
- improve code readability,
- review the README.

All implementation, testing, and debugging were completed by the project members.

---

## Team and Project Management

### Team Members

**odindar**

- Graphical visualizer
- UI integration

**iergin**

- Maze generation algorithm
- Maze solving algorithm

**Shared**

- Configuration parser
- Testing
- Bug fixing

### Planning

We first implemented the configuration parser, then the maze generation algorithm, and finally the graphical visualizer. After all components were working together, we tested the project and fixed bugs.

### What worked well

- Clear division of tasks.
- Easy integration of all project modules.

### What could be improved

- Better code documentation.
- More test cases.
- Additional maze generation algorithms.

### Tools Used

- Python 3
- Git
- GitHub
- Visual Studio Code
- AI
