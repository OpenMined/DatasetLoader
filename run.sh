#!/bin/sh

set -e

if [ ! -d .venv ]; then
  uv venv -p 3.12
fi

. .venv/bin/activate

uv pip install --upgrade syftbox 

echo "Running 'DataSet Loader' with $(python3 --version) at '$(which python3)'"
python3 main.py

deactivate
