refresh: clean build install lint

build:
	python setup.py build

install: 
	python setup.py install

build_dist:
	make clean
	python setup.py sdist bdist_wheel
	pip install dist/*.whl
	make test

release:
	python -m twine upload dist/*

lint:
	flake8 src/ tests/ --count --max-line-length=127 --ignore=W503

test:
	python -m unittest

clean:
	rm -rf __pycache__
	rm -rf tests/__pycache__
	rm -rf src/progshot/__pycache__
	rm -rf build
	rm -rf dist
	rm -rf progshot.egg-info 
	rm -rf src/progshot.egg-info
	pip uninstall -y progshot 
