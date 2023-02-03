#!/bin/sh -e
export PYTHONPATH=.
set -x

# Sort imports one per line, so autoflake can remove unused imports
isort --recursive  --force-single-line-imports --apply app
