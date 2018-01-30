all: clean compile

compile:
	python3.6 setup.py sdist

upload:
	python3.6 setup.py register sdist upload

push:
	git add .
	git commit
	git push origin master

test:
	python tests.py
	python3.6 tests.py

clean:
	find . -name "*.pyc" -type f -delete
	find . -name "__pycache__" -type d -delete
	rm -r *.egg-info || true
	rm -r dist || true
	rm -r build || true
