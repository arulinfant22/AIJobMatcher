# 🆓 Free Deployment Guide for AIJobMatcher

## 🌟 Best Free Deployment Options

### 1. **Render** (Recommended - Easiest)
- **Free Tier**: 750 hours/month
- **Custom Domain**: Free subdomain (your-app.onrender.com)
- **Database**: Free PostgreSQL
- **SSL**: Automatic
- **Limitations**: Sleeps after 15 minutes inactivity

### 2. **PythonAnywhere** (Beginner Friendly)
- **Free Tier**: Basic web app
- **Domain**: Your-username.pythonanywhere.com
- **Database**: SQLite (free) or MySQL (paid)
- **SSL**: Available on free tier
- **Limitations**: Limited CPU and storage

### 3. **Vercel** (Modern & Fast)
- **Free Tier**: 100GB bandwidth/month
- **Domain**: Your-app.vercel.app
- **Database**: Need external free DB
- **SSL**: Automatic
- **Limitations**: Serverless functions

### 4. **Railway** (Developer Friendly)
- **Free Tier**: $5 credit/month
- **Domain**: Your-app.up.railway.app
- **Database**: Free PostgreSQL
- **SSL**: Automatic
- **Limitations**: Credit resets monthly

---

## 🚀 Option 1: Render Deployment (Recommended)

### Step 1: Prepare Your Project
```bash
# Create requirements.txt (already done)
# Create runtime.txt for Python version
echo "python-3.10.8" > runtime.txt

# Create Procfile for web server
echo "web: gunicorn AIJobMatcher.wsgi:application" > Procfile
```

### Step 2: Configure for Render
Create `render.yaml`:
```yaml
services:
  - type: web
    name: aijobmatcher
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn AIJobMatcher.wsgi:application
    envVars:
      - key: DJANGO_SETTINGS_MODULE
        value: AIJobMatcher.production
      - key: PYTHON_VERSION
        value: 3.10.8
```

### Step 3: Deploy to Render
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect your GitHub repository
5. Configure build settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn AIJobMatcher.wsgi:application`
   - **Runtime**: Python 3

### Step 4: Environment Variables
Set these in Render dashboard:
```
DJANGO_SETTINGS_MODULE=AIJobMatcher.production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-app.onrender.com
GOOGLE_API_KEY=your-google-api-key
GOOGLE_CSE_ID=your-google-cse-id
RAPIDAPI_KEY=your-rapidapi-key
RAPIDAPI_HOST=jsearch.p.rapidapi.com
```

### Step 5: Database Setup
1. Add PostgreSQL service in Render
2. Get connection string
3. Update environment variables:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432
```

### Step 6: Run Migrations
```bash
# In Render shell
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

---

## 🐍 Option 2: PythonAnywhere

### Step 1: Sign Up
1. Go to [pythonanywhere.com](https://pythonanywhere.com)
2. Create free account
3. Get your username (this becomes your subdomain)

### Step 2: Upload Files
```bash
# Method 1: Git
git clone <your-repo-url>

# Method 2: Upload via web interface
# Upload all project files
```

### Step 3: Setup Virtual Environment
```bash
# In PythonAnywhere bash console
mkvirtualenv --python=/usr/bin/python3.10 aijobmatcher
pip install -r requirements.txt
```

### Step 4: Configure Web App
1. Go to "Web" tab
2. Add new web app
3. Select "Manual Configuration"
4. Python version: 3.10
5. Set working directory: `/home/yourusername/aijobmatcher`
6. Set virtual environment: `/home/yourusername/.virtualenvs/aijobmatcher`

### Step 5: WSGI Configuration
Edit `/var/www/yourusername_pythonanywhere_com_wsgi.py`:
```python
import os
import sys

path = '/home/yourusername/aijobmatcher'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'AIJobMatcher.production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Step 6: Environment Variables
Set in PythonAnywhere web tab:
```
DJANGO_SETTINGS_MODULE=AIJobMatcher.production
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
```

---

## ⚡ Option 3: Vercel + Supabase

### Step 1: Prepare for Vercel
Create `vercel.json`:
```json
{
  "version": 2,
  "builds": [
    {
      "src": "AIJobMatcher/wsgi.py",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "AIJobMatcher/wsgi.py"
    }
  ]
}
```

### Step 2: Create API Index
Create `api/index.py`:
```python
from django.core.wsgi import get_wsgi_application
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AIJobMatcher.production')
application = get_wsgi_application()
```

### Step 3: Deploy to Vercel
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Step 4: Database (Supabase)
1. Go to [supabase.com](https://supabase.com)
2. Create free account and project
3. Get connection details
4. Update environment variables

---

## 🎯 Option 4: Railway

### Step 1: Install Railway CLI
```bash
npm install -g @railway/cli
```

### Step 2: Deploy
```bash
# Login to Railway
railway login

# Initialize project
railway init

# Deploy
railway up
```

### Step 3: Configure Environment
```bash
# Set environment variables
railway variables set DJANGO_SETTINGS_MODULE=AIJobMatcher.production
railway variables set SECRET_KEY=your-secret-key
railway variables set DEBUG=False
```

---

## 🛠️ Free Database Options

### 1. **Supabase** (Recommended)
- **Free Tier**: 500MB database
- **Features**: PostgreSQL, Auth, Storage
- **Perfect for**: Django projects

### 2. **Neon** 
- **Free Tier**: 3GB database
- **Features**: PostgreSQL, Branching
- **Perfect for**: Development

### 3. **PlanetScale**
- **Free Tier**: 5GB database
- **Features**: MySQL, Branching
- **Perfect for**: MySQL projects

### 4. **SQLite** (Simplest)
- **No external service needed
- **File-based database
- **Perfect for**: Small projects

---

## 🔧 Configuration for Free Platforms

### Update Production Settings
Create `AIJobMatcher/free_settings.py`:
```python
from .production import *

# Free platform optimizations
CONN_MAX_AGE = 60  # Database connection pooling

# Reduce resource usage
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
}

# Cache with file backend (no Redis needed)
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': '/tmp/django_cache',
    }
}

# Session with file backend
SESSION_ENGINE = 'django.contrib.sessions.backends.file'
SESSION_FILE_PATH = '/tmp/sessions'
```

---

## 🌐 Free Domain Options

### 1. **Platform Subdomains** (Easiest)
- `your-app.onrender.com`
- `your-username.pythonanywhere.com`
- `your-app.vercel.app`
- `your-app.up.railway.app`

### 2. **Free DNS Services**
- **No-IP**: Free subdomains
- **FreeDNS**: Free subdomains
- **DNSDynamic**: Free dynamic DNS

### 3. **Tk/Ml/Ga Domains**
- **Freenom**: `.tk`, `.ml`, `.ga`, `.cf`
- **Limitations**: Renewal required
- **Perfect for**: Personal projects

---

## 📋 Quick Start Checklist

### For Render (Recommended):
- [ ] GitHub repository ready
- [ ] `Procfile` created
- [ ] Environment variables set
- [ ] Database configured
- [ ] SSL automatically enabled

### For PythonAnywhere:
- [ ] Account created
- [ ] Files uploaded
- [ ] Virtual environment setup
- [ ] WSGI configured
- [ ] Web app started

### For Vercel:
- [ ] Vercel account created
- [ ] `vercel.json` configured
- [ ] API endpoint created
- [ ] Database connected

---

## 🚨 Free Platform Limitations

### Common Limitations:
- **Sleep time**: Apps sleep after inactivity
- **CPU limits**: Restricted processing power
- **Storage**: Limited disk space
- **Bandwidth**: Monthly data limits
- **Database**: Small free tiers

### Workarounds:
- **Keepalive services**: Prevent sleep
- **Optimize images**: Reduce bandwidth
- **Cache responses**: Improve performance
- **Use CDN**: Offload static files

---

## 🔄 Keep Alive Solutions

### For Render Sleep Prevention:
```python
# Add to urls.py
path('ping/', lambda request: JsonResponse({'status': 'ok'}), name='ping'),
```

### External Keep Alive:
1. **Uptime Robot** (Free)
2. **Pingdom** (Free tier)
3. **GitHub Actions** (Free)

### GitHub Actions Keep Alive:
Create `.github/workflows/keepalive.yml`:
```yaml
name: Keep Alive

on:
  schedule:
    - cron: '*/15 * * * *'  # Every 15 minutes

jobs:
  keep-alive:
    runs-on: ubuntu-latest
    steps:
      - name: Ping app
        run: curl https://your-app.onrender.com/ping/
```

---

## 📊 Performance Optimization

### For Free Platforms:
```python
# Enable compression
MIDDLEWARE += ['django.middleware.gzip.GZipMiddleware']

# Optimize static files
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# Database optimization
DATABASES['default']['CONN_MAX_AGE'] = 60

# Reduce session load
SESSION_SAVE_EVERY_REQUEST = False
```

---

## 🎉 Recommended Choice

**For Beginners**: PythonAnywhere
**For Performance**: Render
**For Modern Stack**: Vercel + Supabase
**For Developers**: Railway

---

**🚀 Your AIJobMatcher is ready for free deployment! Choose the platform that best fits your needs and follow the step-by-step guide above.**
