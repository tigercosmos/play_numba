DOCKER_BUILD_OPTIONS?=
DOCKER_CMD?=

build-docker:
	docker build -f Dockerfile $(DOCKER_BUILD_OPTIONS) -t dboyliao/play-numba:latest .

run-container:
	docker run --rm \
	-it -d -v $$(pwd):/workspace \
	dboyliao/play-numba:latest $(DOCKER_CMD)

setup-container:
	pyenv install -s 3.10.9;
	pyenv global 3.10.9;
	python3 -m pip install -U pip && \
	python3 -m pip install pipenv;
	pyenv rehash;
	virtualenv --python=$$(pyenv which python3) .venv && pipenv install -d;

lib:
	c++ -O3 -Wall -shared -std=c++11 \
	-o libexample$$(python-config --extension-suffix) \
	-fPIC $$(python3 -m pybind11 --includes) \
	example.cpp
