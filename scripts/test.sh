#!/usr/bin/env bash

set -e
set -x
# lint
poetry run black app --check
poetry run isort --recursive --force-single-line-imports --check-only app
poetry run flake8 app
# test
poetry run pytest --cov=app app/tests