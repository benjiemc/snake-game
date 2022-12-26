#!/usr/bin/env bash
set -ex

if [[ -z $VIRTUAL_ENV ]]; then
    python3 -m venv venv
    source venv/bin/activate
fi

pip install -e .[develop]

# pytest || error=1

if [[ $error -ne 1 ]]; then
    flake8 snake_game  || true
fi

exit $error
