#!/usr/bin/env bash
# Exit on error
set -o errexit

# Modify this line to be your package manager of choice.
# For example, 'pip install -r requirements.txt' or 'poetry install'
pip install -r requirements.txt

# Convert all .env files to environment variables for the build process.
# This is useful for when you want to use environment variables in your build process.
# For example, 'DJANGO_SETTINGS_MODULE=mysite.settings.production'
# You can also use this to set other environment variables like 'NODE_ENV=production'
# For example, 'export $(grep -v '^#' .env | xargs)'

# Apply any outstanding database migrations.
python manage.py migrate

# Collect all static files into a single directory.
python manage.py collectstatic --noinput
