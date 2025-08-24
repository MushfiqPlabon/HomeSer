#!/bin/bash
# vercel-setup.sh
# Helper script for initial Vercel setup

echo "HomeSer Vercel Setup Script"
echo "=========================="

# Check if we're running on Vercel
if [[ $VERCEL == "1" ]]; then
    echo "Running on Vercel, executing setup tasks..."
    
    # Collect static files
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
    
    # Check if this is a new deployment
    if [[ $VERCEL_ENV == "production" ]]; then
        echo "Production environment detected"
        # Add any production-specific setup here
    fi
    
    echo "Setup complete!"
else
    echo "Not running on Vercel. Skipping setup tasks."
fi