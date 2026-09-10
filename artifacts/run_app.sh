#!/bin/bash
# Run the Employee Benefits Portal

cd "$(dirname "$0")/.."

echo "Starting Employee Benefits Portal..."
echo "Database will be initialized at: generated_app/database.db"

python -m uvicorn generated_app.main:app --host 0.0.0.0 --port 8000 --reload
