#!/bin/bash
set -e

export PGPASSWORD="${POSTGRES_PASSWORD:-password}"

# Wait for the database to be ready
until pg_isready -h user_db -p 5432 -U postgres; do
  echo "Waiting for user_db to be ready..."
  sleep 2
done

alembic upgrade head
# Optional: run some SQL setup (if needed)
# psql -h user_db -U user_service -d user_service -c "SELECT 1;"

# Start the app
exec uvicorn main:app --host 0.0.0.0 --port 8000
