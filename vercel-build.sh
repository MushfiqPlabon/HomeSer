#!/bin/bash
# Build script for Vercel deployment

# Install dependencies
pip install -r requirements.txt

# Run Django collectstatic (though we don't have static files, this is a standard Django step)
# python manage.py collectstatic --noinput

# Run migrations
# python manage.py migrate --noinput