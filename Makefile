PYTHON = python3
PIP = pip3
MAIN = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug clean fclean re lint lint-strict build

all: run

install:
	$(PIP) install --upgrade pip
	$(PIP) install flake8 mypy build
	$(PIP) install -e .

build:
	$(PYTHON) -m build --wheel

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	rm -rf __pycache__ .mypy_cache */__pycache__
	rm -rf *.egg-info build dist

fclean: clean
	rm -f maze.txt

re: fclean all

lint:
	flake8 .
	mypy --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs .

lint-strict:
	flake8 .
	mypy --strict .
