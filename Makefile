.DEFAULT_GOAL := build
format:
	find . -name "*.py" -exec black {} ';'

test:
	pytest tests/

build:
	format
	test