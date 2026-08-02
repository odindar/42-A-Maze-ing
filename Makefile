PYTHON = python3
PIP = pip3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean fclean re lint lint-strict

all: run

install:
	$(PIP) install rich flake8 mypy prompt_toolkit

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache
	rm -rf */__pycache__

fclean: clean
	rm -f maze.txt output_maze.txt

re: fclean all

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .
