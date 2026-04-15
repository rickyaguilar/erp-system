#!/usr/bin/env bash
set -e

pip install -r requirements.txt

echo "RUNNING MIGRATIONS..."
python manage.py migrate --verbosity 3