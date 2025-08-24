#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

echo "Starting custom build process..."

# Create a virtual environment
python3.10 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip wheel

# Install dependencies
pip install -r requirements.txt

# Run collectstatic
python manage.py collectstatic --noinput --clear

echo "Custom build process finished."