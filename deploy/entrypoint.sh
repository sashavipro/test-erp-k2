#!/bin/sh
set -e

# Run migrations
alembic upgrade head

# Start the application
exec uvicorn src.main:app --host 0.0.0.0 --port 8000
