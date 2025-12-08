# DEPLOYMENT GUIDE FOR ERP SYSTEM

## Quick Start - Deploy to Render.com (Recommended)

### Step 1: Prepare Your Code
1. Make sure all files are saved
2. Create a GitHub account if you don't have one
3. Create a new repository on GitHub

### Step 2: Push to GitHub
```bash
cd /home/riks/projects/erp_system
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com and sign up (free)
2. Click "New +" → "Web Service"
3. Connect your GitHub account
4. Select your repository
5. Configure:
   - **Name:** erp-system (or any name)
   - **Environment:** Python 3
   - **Build Command:** `./build.sh`
   - **Start Command:** `gunicorn erp_system.wsgi:application`
6. Add Environment Variables:
   - `SECRET_KEY` = (generate a new one)
   - `DEBUG` = False
   - `DATABASE_URL` = (Render provides this automatically)
7. Click "Create Web Service"

### Step 4: Add PostgreSQL Database
1. In Render dashboard, click "New +" → "PostgreSQL"
2. Name it `erp-database`
3. Click "Create Database"
4. Copy the "Internal Database URL"
5. Go back to your Web Service
6. Add environment variable: `DATABASE_URL` = (paste the URL)

### Step 5: Update Settings (Already Done)
The files are ready:
- ✅ `requirements.txt` - Dependencies
- ✅ `build.sh` - Build script
- ✅ `Procfile` - Run command
- ✅ `runtime.txt` - Python version

---

## Alternative: PythonAnywhere

### Steps:
1. Sign up at https://www.pythonanywhere.com
2. Go to "Web" tab
3. Click "Add a new web app"
4. Choose "Manual configuration" → Python 3.12
5. Upload your files or use Git:
   ```bash
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
   ```
6. Set up virtual environment:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.12 myenv
   pip install -r requirements.txt
   ```
7. Configure WSGI file (PythonAnywhere provides template)
8. Set up static files in Web tab
9. Reload your web app

Your site will be at: `YOUR_USERNAME.pythonanywhere.com`

---

## Important Production Updates Needed:

### 1. Update settings.py for production
Add to settings.py:
```python
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*').split(',')

# Database - use PostgreSQL in production
if 'DATABASE_URL' in os.environ:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL')
        )
    }

# Static files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### 2. Generate New SECRET_KEY
Run in terminal:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## Cost Comparison:

| Platform | Free Tier | Database | Custom Domain |
|----------|-----------|----------|---------------|
| **Render** | 750 hrs/month | PostgreSQL Free | Yes |
| **PythonAnywhere** | Always on | MySQL Free | yourusername.pythonanywhere.com |
| **Railway** | $5/month credit | PostgreSQL | Yes |
| **Heroku** | No longer free | - | - |

---

## My Recommendation:
**Use Render.com** - It's the easiest and most reliable for Django apps!

After deployment, you can access your app from anywhere at:
`https://your-app-name.onrender.com`

Need help with any step?
