#!/bin/sh
echo "Applying migrations..."
uv run alembic upgrade head

echo "Starting backend..."
exec uv run python -m src.backend.main.main