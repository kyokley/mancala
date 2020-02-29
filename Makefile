.PHONY: autoformat tests

autoformat:
	docker run --rm -it -v $(pwd):/code kyokley/mancala /bin/bash -c " \
	git ls-files | grep -P '\.py$$' | xargs isort && \
	git ls-files | grep -P '\.py$$' | xargs black -S && \
	"

tests:
	docker run --rm -it -v $(pwd):/code kyokley/mancala /bin/bash -c " \
	pytest && \
	git ls-files | grep -P '\.py$$' | xargs black -S --check && \
	git ls-files | grep -P '\.py$$' | xargs flake8 --select F821,F401 \
	"

build:
	docker build -t kyokley/mancala .

build-dev:
	docker build --build-arg REQS=dev -t kyokley/mancala .

run:
	docker run --rm -it -v $(pwd):/code kyokley/mancala

game: run
