#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt
npm install
npx @tailwindcss/cli -i static/css/main.css -o static/dist/css/output.css --minify

# Run migrations and collect static files
python manage.py migrate

python manage.py collectstatic --noinput
