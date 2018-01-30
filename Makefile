all: clean compile

compile: test clean
	python3.6 setup.py sdist

upload: compile
	twine upload dist/*

test:
	python3.6 tests.py

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "__pycache__" -type d -delete
	rm -r *.egg-info || true
	rm -r dist || true
	rm -r build || true
