format:
	isort .
	black .

check:
	isort --check-only --diff .
	black --check .
	flake8 --config=.flake8


install:
	python3 -m pip install flit
	flit install


test:
	pytest
