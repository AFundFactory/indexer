.ONESHELL:
.PHONY: $(MAKECMDGOALS)
##
##    🚧 DipDup developer tools
##
## DEV=1                Whether to install dev dependencies
DEV=1
## TAG=latest           Tag for the `image` command
TAG=latest

##

help:           ## Show this help (default)
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/##//'

all:            ## Run a whole CI pipeline: formatters, linters and tests
	make install lint test

install:        ## Install project dependencies
	poetry install \
	`if [ "${DEV}" = "0" ]; then echo "--no-dev"; fi`

lint:           ## Lint with all tools
	make isort black flake mypy

test:           ## Run test suite
	poetry run pytest tests

##

isort:          ## Format with isort
	poetry run isort src tests

black:          ## Format with black
	poetry run black src tests

flake:          ## Lint with flake8
	poetry run flakeheaven lint src tests

mypy:           ## Lint with mypy
	poetry run mypy src tests

build:          ## Build Python wheel package
	poetry build

image:          ## Build Docker image
	docker buildx build . -t indexer:${TAG}

clean:          ## Remove all files from .gitignore except for `.venv`
	git clean -xdf --exclude=".venv"

##