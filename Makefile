NAME = a_maze_ing.py
CONFIG = config.txt

install:
	uv sync

run:
	uv run $(NAME) $(CONFIG)

clean:
	uv cache clean
	rm -rf __pycache__ .mypy_cache .venv uv.lock


lint:
	- flake8 .
	- mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	- flake8 .
	- mypy . --strict
