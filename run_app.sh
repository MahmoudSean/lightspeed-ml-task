#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

echo "🚀 Starting fastapi app launching ..."

# Optional: set PYTHONPATH to allow local imports from src/
export PYTHONPATH=$(pwd)

if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "⚠️  Could not activate virtualenv. Continuing..."
fi

uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

echo "✅ App launched successfully."