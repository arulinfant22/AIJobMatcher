#!/bin/bash

# Script to collect static files for deployment
echo "🚀 Collecting static files for AIJobMatcher deployment..."

# Activate virtual environment if it exists
if [ -d "env" ]; then
    source env/bin/activate
fi

# Collect static files
echo "📁 Running collectstatic..."
python manage.py collectstatic --noinput --clear

# Check if staticfiles directory was created
if [ -d "staticfiles" ]; then
    echo "✅ Static files collected successfully!"
    echo "📊 Static files summary:"
    find staticfiles -type f | wc -l | xargs echo "Total files:"
    du -sh staticfiles | xargs echo "Total size:"
    
    echo ""
    echo "📂 Directory structure:"
    tree staticfiles -L 2 2>/dev/null || find staticfiles -type d | head -10
else
    echo "❌ Failed to create staticfiles directory"
    exit 1
fi

echo ""
echo "🎯 Static files are ready for deployment!"
echo "📝 Make sure your deployment platform serves files from /static/"
