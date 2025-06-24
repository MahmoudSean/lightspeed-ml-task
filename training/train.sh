#!/bin/bash

echo "🚀 Starting training..."

# Load environment variables
if [ -f .env ]; then
  export $(grep -v '^#' .env | xargs)
  echo "✅ Loaded .env variables"
else
  echo "⚠️  No .env file found. Skipping env var load."
fi

# Activate virtualenv (Windows-friendly)
if [ -f ".venv/Scripts/activate" ]; then
  source .venv/Scripts/activate
elif [ -f ".venv/bin/activate" ]; then
  source .venv/bin/activate
else
  echo "⚠️  Could not activate virtualenv. Continuing..."
fi

# 🔥 Fix for src import
export PYTHONPATH=$(pwd)

# Run training
python training/train_model.py

echo "✅ Training completed."
