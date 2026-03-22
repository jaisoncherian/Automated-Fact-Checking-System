# 🚀 VeriNews AI - Complete Deployment Guide

This guide shows you how to run VeriNews AI locally and deploy it to production.

---

## 📋 Table of Contents

1. [Quick Start (Local)](#quick-start-local)
2. [Architecture Overview](#architecture-overview)
3. [Running All Services](#running-all-services)
4. [Production Deployment](#production-deployment)
5. [Service Configuration](#service-configuration)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start (Local)

### ✅ Prerequisites

- Python 3.8+ installed
- MongoDB Atlas account with connection string in `.env`
- Virtual environment activated (see [FULL_SETUP_GUIDE.md](FULL_SETUP_GUIDE.md))

### 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 🗄️ Populate Database

First, ensure MongoDB has fact data:

```bash
cd backend
python insert_data.py
```

Expected output:
```
✓ Connected to MongoDB
✓ Inserted 3 facts into MongoDB
```

### ▶️ Run All Services (Local)

Open **4 separate terminals** in the project root:

#### Terminal 1: FastAPI Backend
```bash
cd backend
python -m uvicorn api:app --reload --port 8000
```
✓ Runs on: **http://127.0.0.1:8000**
✓ Swagger UI: **http://127.0.0.1:8000/docs**

#### Terminal 2: Streamlit Interactive App
```bash
streamlit run frontend/app.py
```
✓ Runs on: **http://localhost:8501**
✓ Best for: Interactive fact-checking interface

#### Terminal 3: Flask Landing Page
```bash
cd frontend
python server.py
```
✓ Runs on: **http://localhost:5000**
✓ Best for: Marketing/info landing page

#### Terminal 4: Optional - Monitor Logs
```bash
# Just keep this terminal free for viewing logs
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    USER DEVICES                          │
│                                                           │
│  ┌──────────────┐    ┌──────────────┐  ┌──────────────┐ │
│  │   Desktop    │    │   Mobile     │  │   API Users  │ │
│  │  (Browser)   │    │  (Browser)   │  │ (Developers) │ │
│  └──────────────┘    └──────────────┘  └──────────────┘ │
└──────┬──────────────────────────┬───────────────────────┘
       │                          │
       │                          │
    Port 5000               Port 8501              Port 8000
       │                          │                    │
    ┌──▼──────────┐    ┌─────────▼──┐     ┌──────────▼────┐
    │   Landing    │    │ Streamlit  │     │  FastAPI      │
    │    Page      │    │   App      │     │   Backend     │
    │  (Flask)     │    │(Interactive)     │  (REST API)   │
    └──┬──────────┘    └──────┬────┘      └────┬──────────┘
       │                      │                 │
       │      ┌─────────────────────┐      ┌────┤
       │      │  Fact-Checking      │      │
       │      │  Engine             │      │
       │      │ (Sentence           │◄─────┘
       │      │  Transformers +     │
       │      │  Cosine Similarity) │
       │      └──────────┬──────────┘
       │                 │
       └────────────┬────┘
                    │
        ┌───────────▼──────────┐
        │   MongoDB Atlas      │
        │   Cloud Database     │
        │   (fact_checker DB)  │
        └──────────────────────┘
```

---

## Running All Services

### Step 1: Prepare Environment

```bash
# Navigate to project root
cd c:\Users\jaison\Automated-Fact-Checking-System

# Activate virtual environment
venv\Scripts\Activate.ps1
```

### Step 2: Check MongoDB Connection

```bash
python -c "from backend.db import collection; print('✓ MongoDB connected')"
```

### Step 3: Populate Database (First Time Only)

```bash
python backend/insert_data.py
```

### Step 4: Start All Three Services

Use Windows Terminal or PowerShell with multiple tabs:

**Tab 1 - FastAPI Backend:**
```bash
cd backend
python -m uvicorn api:app --reload --port 8000
```

**Tab 2 - Streamlit App:**
```bash
streamlit run frontend/app.py
```

**Tab 3 - Flask Landing Page:**
```bash
cd frontend
python server.py
```

### Step 5: Verify All Services

| Service | URL | Purpose |
|---------|-----|---------|
| Landing Page | http://localhost:5000 | Marketing/Info site |
| Fact-Checker | http://localhost:8501 | Interactive tool |
| API Backend | http://127.0.0.1:8000 | REST API |
| API Docs | http://127.0.0.1:8000/docs | Swagger playground |

### Step 6: Test Full Flow

1. Open **http://localhost:5000** (landing page)
2. Click **"Try It Free"** or **"Start Verifying"**
3. Gets redirected to **http://localhost:8501** (Streamlit app)
4. Enter a test claim: `"earth is flat"` or `"india capital is delhi"`
5. Click **"Check Fact"** button
6. See result with confidence score

---

## Production Deployment

### 🌐 Deploy Landing Page + Frontend

#### Option A: Vercel (Recommended for Flask)

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Create `vercel.json` in frontend folder:**
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "server.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "server.py"
       }
     ],
     "env": {
       "FLASK_ENV": "production"
     }
   }
   ```

3. **Deploy:**
   ```bash
   cd frontend
   vercel deploy --prod
   ```

#### Option B: Netlify (For Static HTML)

1. **Drag & drop your `frontend/` folder to Netlify**
2. **Or use CLI:**
   ```bash
   npm install -g netlify-cli
   cd frontend
   netlify deploy --prod --dir=.
   ```

### 🔌 Deploy Backend API

#### Option A: Railway (Easy, Free Tier)

1. **Create account on Railway.app**
2. **Connect GitHub repo**
3. **Set environment variables:**
   - `MONGODB_URI`: Your MongoDB Atlas connection string
   - `PORT`: 8000

4. **Deploy:**
   ```bash
   # Just push to GitHub, Railway auto-deploys
   git push origin main
   ```

#### Option B: Heroku (Cloud Platform)

1. **Install Heroku CLI:**
   ```bash
   choco install heroku-cli
   ```

2. **Create `Procfile` in project root:**
   ```
   web: cd backend && gunicorn -w 4 -b 0.0.0.0:$PORT api:app
   ```

3. **Login and deploy:**
   ```bash
   heroku login
   heroku create verinews-ai-backend
   heroku config:set MONGODB_URI="your_mongodb_connection_string"
   git push heroku main
   ```

#### Option C: AWS EC2 (Full Control)

1. **Launch an EC2 instance (Ubuntu 20.04)**
2. **SSH into instance:**
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-ip
   ```

3. **Setup Python & dependencies:**
   ```bash
   sudo apt update && sudo apt install python3 python3-pip
   git clone your-repo
   cd Automated-Fact-Checking-System
   pip install -r requirements.txt
   ```

4. **Run with Gunicorn & Nginx:**
   ```bash
   cd backend
   gunicorn -w 4 -b 0.0.0.0:8000 api:app
   ```

### 🎨 Deploy Streamlit App

#### Streamlit Cloud (Official & Free)

1. **Push code to GitHub**
2. **Go to share.streamlit.io**
3. **Connect GitHub repo**
4. **Select `frontend/app.py` as main file**
5. **Click "Deploy"**

Streamlit handles hosting automatically!

---

## Service Configuration

### 📝 Environment Variables (.env)

Create `.env` file in project root:

```env
# MongoDB Connection
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/?appName=Cluster0

# Optional: Backend settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# Optional: Flask settings
FLASK_ENV=production
```

### 🔐 Update Links for Production

After deployment, update all hardcoded localhost URLs:

**In `frontend/index.html`:**
```html
<!-- Change from: -->
<a href="http://localhost:8501">Start Verifying →</a>
<a href="http://127.0.0.1:8000/docs">API Docs</a>

<!-- To: -->
<a href="https://verinews-app.streamlit.app">Start Verifying →</a>
<a href="https://api.verinews.com/docs">API Docs</a>
```

**In `frontend/app.py`:**
```python
# Change from:
response = requests.post("http://127.0.0.1:8000/check", ...)

# To:
response = requests.post("https://api.verinews.com/check", ...)
```

---

## Troubleshooting

### ❌ **Port Already in Use**

```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or use different port
python -m uvicorn backend.api:app --port 8001
```

### ❌ **MongoDB Connection Failed**

```bash
# Check connection string
python -c "from backend.db import collection; print('✓ Connected')"

# If fails:
# 1. Verify .env file has MONGODB_URI
# 2. Check MongoDB Atlas whitelist IPs
# 3. Confirm credentials are correct
```

### ❌ **Streamlit Can't Connect to Backend**

```bash
# Ensure FastAPI is running:
curl http://127.0.0.1:8000/

# Should return:
# {"message":"Fake News Detection API Running"}

# If not running, start it:
python -m uvicorn backend.api:app --reload
```

### ❌ **CORS Issues in Production**

Update `backend/api.py` to allow cross-origin requests:

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### ⚠️ **Sentiment Analysis Returns Empty**

Ensure Sentence Transformers model is downloaded:

```bash
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"
```

---

## Performance Tips

### 🚀 Backend Optimization

```bash
# Use production ASGI server
pip install gunicorn
gunicorn -w 4 -k uvicorn.workers.UvicornWorker backend.api:app

# Or with more workers
gunicorn -w $(nproc) -k uvicorn.workers.UvicornWorker backend.api:app
```

### 💾 Database Optimization

```javascript
// Create index in MongoDB for faster searches
db.facts.createIndex({ "claim": "text" })
```

### 🔄 Caching

Add Redis for caching frequently checked claims:

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def check_fact(user_input):
    # ... fact checking logic
    pass
```

---

## Monitoring & Logging

### 📊 Local Development Logs

```bash
# View Streamlit logs
streamlit run frontend/app.py --logger.level=debug

# View FastAPI logs with timestamps
python -m uvicorn backend.api:app --log-level debug
```

### ☁️ Production Monitoring

Set up alerts on your hosting provider:

- **Railway**: Dashboard → Monitoring → Alerts
- **Heroku**: Heroku Dashboard → Settings → Logging
- **Streamlit Cloud**: View logs in deployment settings

---

## Summary

### 🎯 Local Testing Checklist

- [ ] MongoDB connection verified
- [ ] Database populated with facts
- [ ] FastAPI backend running (port 8000)
- [ ] Streamlit app running (port 8501)
- [ ] Flask landing page running (port 5000)
- [ ] Test end-to-end flow works
- [ ] All buttons link correctly

### 🌐 Production Checklist

- [ ] Landing page deployed
- [ ] Backend API deployed with HTTPS
- [ ] Streamlit Cloud app deployed
- [ ] Environment variables set
- [ ] All URLs updated (no localhost references)
- [ ] CORS configured
- [ ] Database connection tested in production
- [ ] Log monitoring enabled
- [ ] Backups configured

---

## Next Steps

1. **Add more facts** to MongoDB for better accuracy
2. **Implement authentication** for API endpoints
3. **Set up GitHub Actions** for CI/CD
4. **Add rate limiting** to prevent abuse
5. **Implement caching** for performance
6. **Add analytics** to track usage
7. **Create admin dashboard** for managing facts

---

## Support

For issues or questions:
- Check [FULL_SETUP_GUIDE.md](FULL_SETUP_GUIDE.md) for initial setup
- Review [MONGODB_SETUP.md](MONGODB_SETUP.md) for database help
- Check API docs at: http://127.0.0.1:8000/docs (when running locally)

---

**Happy deploying! 🚀**
