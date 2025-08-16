#!/bin/sh

# Exit immediately if a command exits with a non-zero status
set -e

echo "🔧 Installing system dependencies..."
sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3

echo "🐍 Creating virtual environment..."
python3 -m venv venv

echo "✅ Activating virtual environment..."
. venv/bin/activate

echo "📦 Upgrading pip and installing Python dependencies..."
pip install --upgrade pip

# If you have a requirements.txt, install from it; otherwise, list your packages here
if [ -f requirements.txt ]; then
    pip install -r requirements.txt
else
    pip install flask pytest
fi

# Make project root importable
export PYTHONPATH="$(pwd)"

# Ensure db directory exists
mkdir -p db

# Always start with a fresh DB
if [ -f db/gitgrub.sqlite3 ]; then
  echo "🗑️  Removing old database..."
  rm db/gitgrub.sqlite3
fi

# Run seed to create schema + seed data
echo "🌱 Seeding database..."
python seed.py

echo "✅ Setup complete. Run 'flask run' to start the app."

