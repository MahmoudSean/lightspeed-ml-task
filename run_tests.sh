#!/bin/bash

echo "🔍 Running all tests with pytest..."

# Optional: set PYTHONPATH to allow local imports from src/
export PYTHONPATH=$(pwd)

if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "⚠️  Could not activate virtualenv. Continuing..."
fi

pytest tests/ --disable-warnings -v

echo "✅ All tests completed."
