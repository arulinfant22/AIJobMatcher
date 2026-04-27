# AIJobMatcher Deployment Guide

## 🚀 Deployment Options

### Option 1: VPS Deployment (Recommended for Full Control)
- **DigitalOcean** ($6-20/month)
- **Vultr** ($6-20/month)
- **Linode** ($5-20/month)
- **AWS EC2** (Free tier available)

### Option 2: PaaS (Platform as a Service)
- **Heroku** (Easy but expensive)
- **PythonAnywhere** (Beginner-friendly)
- **Render** (Modern, good free tier)

### Option 3: Docker Deployment
- **Docker + Docker Compose**
- **Portainer** for management

---

## 📋 Prerequisites

### Domain & SSL
- Purchase a domain name
- Set up DNS records
- Obtain SSL certificate (Let's Encrypt recommended)

### Server Requirements
- Ubuntu 20.04+ or CentOS 8+
- 2GB RAM minimum
- 20GB storage minimum
- Python 3.8+

---

## 🔧 VPS Deployment Steps

### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib redis-server -y

# Install Certbot for SSL
sudo apt install certbot python3-certbot-nginx -y
```

### 2. Database Setup
```bash
# Create PostgreSQL database
sudo -u postgres psql
CREATE DATABASE aijobmatcher_prod;
CREATE USER your_db_user WITH PASSWORD 'your_db_password';
GRANT ALL PRIVILEGES ON DATABASE aijobmatcher_prod TO your_db_user;
\q
```

### 3. Application Deployment
```bash
# Clone your repository
git clone <your-repo-url> /var/www/aijobmatcher
cd /var/www/aijobmatcher

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn psycopg2-binary redis

# Setup environment
cp .env.example .env
# Edit .env with your production values
```

### 4. Configure Django
```bash
# Set production settings
export DJANGO_SETTINGS_MODULE=AIJobMatcher.production

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Create superuser
python manage.py createsuperuser
```

### 5. Configure Gunicorn
```bash
# Copy and configure gunicorn service
sudo cp gunicorn.service /etc/systemd/system/
# Edit paths in the service file
sudo nano /etc/systemd/system/gunicorn.service

# Enable and start gunicorn
sudo systemctl daemon-reload
sudo systemctl enable gunicorn
sudo systemctl start gunicorn
```

### 6. Configure Nginx
```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/aijobmatcher
sudo ln -s /etc/nginx/sites-available/aijobmatcher /etc/nginx/sites-enabled/

# Test and restart nginx
sudo nginx -t
sudo systemctl restart nginx
```

### 7. SSL Certificate
```bash
# Obtain SSL certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Set up auto-renewal
sudo crontab -e
# Add: 0 12 * * * /usr/bin/certbot renew --quiet
```

---

## 🐳 Docker Deployment (Alternative)

### Dockerfile
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "AIJobMatcher.wsgi:application"]
```

### docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DJANGO_SETTINGS_MODULE=AIJobMatcher.production
    depends_on:
      - db
      - redis

  db:
    image: postgres:13
    environment:
      POSTGRES_DB: aijobmatcher_prod
      POSTGRES_USER: your_db_user
      POSTGRES_PASSWORD: your_db_password
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:6-alpine

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./staticfiles:/static
      - ./ssl:/etc/ssl/certs
    depends_on:
      - web

volumes:
  postgres_data:
```

---

## 🌐 PaaS Deployment

### Heroku
```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-app-name

# Set environment variables
heroku config:set DJANGO_SETTINGS_MODULE=AIJobMatcher.production
heroku config:set SECRET_KEY=your-secret-key
# Set other env vars...

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate
```

### Render
1. Connect your GitHub repository
2. Set environment variables
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `gunicorn AIJobMatcher.wsgi:application`

---

## 🔍 Health Monitoring

### Health Check Endpoint
Add to `urls.py`:
```python
path('health/', lambda request: JsonResponse({'status': 'healthy'}), name='health'),
```

### Monitoring Tools
- **Uptime Robot** (Free)
- **Pingdom** (Paid)
- **New Relic** (Free tier)

---

## 📊 Performance Optimization

### Database Optimization
```python
# Add indexes to models
class userlogin(models.Model):
    username = models.CharField(max_length=100, unique=True, db_index=True)
    email = models.EmailField(max_length=255, null=True, db_index=True)
```

### Caching
```python
# Cache expensive operations
from django.core.cache import cache

def get_job_listings(keywords):
    cache_key = f"jobs_{'_'.join(keywords)}"
    jobs = cache.get(cache_key)
    if jobs is None:
        jobs = fetch_jobs_from_api(keywords)
        cache.set(cache_key, jobs, 3600)  # Cache for 1 hour
    return jobs
```

---

## 🔒 Security Checklist

- [ ] SECRET_KEY is secure and not in code
- [ ] DEBUG = False in production
- [ ] HTTPS/SSL configured
- [ ] Database credentials secure
- [ ] API keys in environment variables
- [ ] Regular backups configured
- [ ] Firewall configured
- [ ] Log monitoring set up
- [ ] Rate limiting implemented
- [ ] File upload validation

---

## 🚨 Troubleshooting

### Common Issues

#### 502 Bad Gateway
```bash
# Check gunicorn status
sudo systemctl status gunicorn
# Check logs
sudo journalctl -u gunicorn
```

#### Database Connection Issues
```bash
# Check PostgreSQL status
sudo systemctl status postgresql
# Test connection
psql -h localhost -U your_db_user -d aijobmatcher_prod
```

#### Static Files Not Loading
```bash
# Check permissions
sudo chown -R www-data:www-data /var/www/aijobmatcher/staticfiles
# Recollect static files
python manage.py collectstatic --noinput --clear
```

---

## 📦 Maintenance

### Regular Tasks
```bash
# Update dependencies
pip freeze > requirements.txt

# Backup database
pg_dump aijobmatcher_prod > backup_$(date +%Y%m%d).sql

# Clear logs
truncate -s 0 /var/log/nginx/error.log
```

### Monitoring Commands
```bash
# Server resources
htop
df -h
free -h

# Application logs
tail -f /var/log/nginx/access.log
tail -f /var/log/nginx/error.log
journalctl -u gunicorn -f
```

---

## 🆘 Support

### Getting Help
- Check logs: `/var/log/nginx/error.log`, `journalctl -u gunicorn`
- Test locally: `python manage.py runserver`
- Community: Stack Overflow, Django forums

### Emergency Rollback
```bash
# Rollback to previous commit
git checkout <previous-commit-hash>
sudo systemctl restart gunicorn
```

---

**🎉 Your AIJobMatcher application is now ready for production deployment!**

Choose the deployment method that best fits your needs and budget. For beginners, I recommend starting with a PaaS like Render or PythonAnywhere. For full control and better performance, choose VPS deployment.
