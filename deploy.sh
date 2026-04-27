#!/bin/bash

# AIJobMatcher Deployment Script
# This script helps deploy the Django application to production

set -e  # Exit on any error

echo "🚀 Starting AIJobMatcher Deployment..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt
pip install gunicorn psycopg2-binary redis

# Create necessary directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p staticfiles
mkdir -p media

# Set environment variables
echo "⚙️ Setting environment..."
export DJANGO_SETTINGS_MODULE=AIJobMatcher.production

# Collect static files
echo "🗂️ Collecting static files..."
python manage.py collectstatic --noinput

# Run database migrations
echo "🗄️ Running database migrations..."
python manage.py migrate

# Create superuser if needed (optional)
echo "👤 Creating superuser (optional)..."
# python manage.py createsuperuser

# Restart application server
echo "🔄 Restarting application server..."
sudo systemctl restart gunicorn
sudo systemctl restart nginx

echo "✅ Deployment completed successfully!"
echo "🌐 Your application should now be live!"

# Health check
echo "🏥 Running health check..."
curl -f http://localhost:8000/ || echo "⚠️ Health check failed - check logs"
