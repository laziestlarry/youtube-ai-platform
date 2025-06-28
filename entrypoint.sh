#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations against the local SQLite database
echo "Running database migrations..."
alembic upgrade head

# Start the main application using supervisor
echo "Starting supervisord..."
exec /usr/bin/supervisord