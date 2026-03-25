#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt


python manage.py collectstatic --no-input


mkdir -p media

# Run database migrations
python manage.py migrate