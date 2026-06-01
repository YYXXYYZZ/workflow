#!/usr/bin/env sh
set -eu

uv run uvicorn src.task_api.main:app --reload --host 127.0.0.1 --port 8000
