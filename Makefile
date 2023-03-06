DOCKER_BUILD_OPTIONS?=
DOCKER_CMD?=

build-docker:
	docker build -f Dockerfile $(DOCKER_BUILD_OPTIONS) -t dboyliao/play-numba:latest .

run-container:
	docker run --rm \
	-it -d -v $$(pwd):/workspace \
	dboyliao/play-numba:latest $(DOCKER_CMD)

lib:
	c++ -O3 -Wall -shared -std=c++11 \
	-o libexample$$(python-config --extension-suffix) \
	-fPIC $$(python3 -m pybind11 --includes) \
	example.cpp
