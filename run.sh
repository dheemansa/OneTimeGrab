#!/bin/bash
set -e

if [ "$1" == "--new" ]; then
    python3 new_session.py
fi

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
cd "$SCRIPT_DIR"

if ! command -v python3 &> /dev/null; then
    echo "Python3 is not installed. Please install it first."
    exit 1
fi

if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install it first."
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "The .env file does not exist. Running setup..."
    python3 setup.py
fi

git stash || true
git pull || true
git stash pop || true

# Try to install/upgrade required Python packages
if ! pip install -r requirements.txt; then
    echo "Warning: Could not update Python packages. You may encounter issues if requirements are not satisfied."
fi


echo "Running the application..."
python3 -m src.main

echo "Done."