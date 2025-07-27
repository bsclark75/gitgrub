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

echo "✅ Setup complete. Virtual environment activated."
