#!/usr/bin/env bash

source venv/bin/activate
set -a
. .env
set +a
python3 main.py