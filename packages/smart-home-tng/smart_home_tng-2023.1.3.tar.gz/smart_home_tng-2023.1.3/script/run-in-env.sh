#!/usr/bin/bash

set -eu

# Activate pyenv and virtualenv if present, then run the specified command

# pyenv, pyenv-virtualenv
if [ -s .python-version ]; then
    PYENV_VERSION=$(head -n 1 .python-version)
    export PYENV_VERSION
fi

# other common virtualenvs
#my_path=$(git rev-parse --show-toplevel)

for venv in venv .venv . ~/.venv; do
  if [ -f "${venv}/${PYENV_VERSION}/bin/activate" ]; then
      source "${venv}/${PYENV_VERSION}/bin/activate"
    break
  fi
  if [ -f "${venv}/bin/activate" ]; then
      source "${venv}/bin/activate"
    break
  fi
done

PYTHONPATH=".:../home-assistant-core"
export PYTHONPATH

exec "$@"
