format:
	find . -name "*.py" -exec black {} +

test:
	pytest tests/