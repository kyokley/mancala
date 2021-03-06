.PHONY: publish game run build-dev build tests autoformat shell

autoformat: build-dev
	docker run --rm -t -v $$(pwd):/workspace kyokley/mancala /bin/bash -c " \
	git ls-files | grep -P '\.py$$' | xargs isort -m 3 -tc && \
	git ls-files | grep -P '\.py$$' | xargs black -S \
	"

tests: build-dev test-pytest check-formatting

test-pytest: build-dev
	docker run --rm -t -v $$(pwd):/workspace kyokley/mancala /bin/bash -c "pytest"

check-formatting: build-dev
	docker run --rm -t -v $$(pwd):/workspace kyokley/mancala /bin/bash -c " \
	git ls-files | grep -P '\.py$$' | xargs black -S --check && \
	git ls-files | grep -P '\.py$$' | xargs flake8 --select F821,F401 \
	"

build:
	docker build --target=prod -t kyokley/mancala .

build-dev:
	docker build --target=dev -t kyokley/mancala .

run:
	docker run --rm -it -v $$(pwd):/workspace kyokley/mancala

game: run

publish: build
	docker push kyokley/mancala

shell:
	docker run --rm -it -v $$(pwd):/workspace kyokley/mancala /bin/bash
