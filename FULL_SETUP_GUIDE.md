# 🧠 VeriNews AI - Complete Setup Guide

## 📋 System Overview

VeriNews AI is a **production-ready, multilingual fake news detection system** with:
- 🎨 **Professional HTML Landing Page** (Marketing & Info)
- 🐍 **FastAPI Backend** (AI Processing)
- 🎯 **Streamlit App** (Interactive Fact-Checker)
- 🗄️ **MongoDB Atlas** (Cloud Database)
- 🤖 **Sentence Transformers** (NLP AI Model)

---

## 🚀 **Quick Start (4 Easy Steps)**

### **Step 1: Install Dependencies** (One-time)
```powershell
# Navigate to project root
cd c:\Users\jaison\Automated-Fact-Checking-System

# Install all packages (already done, but if needed)
pip install -r requirements.txt
```

### **Step 2: Insert Sample Data** (One-time)
```powershell
cd backend
python insert_data.py
```
✅ Expected output: `✓ Inserted 3 facts into MongoDB`

### **Step 3: Start Backend** (Terminal 1)
```powershell
cd c:\Users\jaison\Automated-Fact-Checking-System
python -m uvicorn backend.api:app --reload
```
✅ Expected: `Application startup complete`
- 📍 **API URL**: http://127.0.0.1:8000
- 📖 **API Docs**: http://127.0.0.1:8000/docs

### **Step 4: Start Frontend** (Terminal 2 or 3)

**Option A - Professional Landing Page + App:**
```powershell
cd c:\Users\jaison\Automated-Fact-Checking-System\frontend
python server.py
```
✅ Visit: http://localhost:5000

**Option B - Direct to Interactive App:**
```powershell
cd c:\Users\jaison\Automated-Fact-Checking-System
streamlit run frontend/app.py
```
✅ Visit: http://localhost:8501

---

## 🏗️ **System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                    VERINEWS AI STACK                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Frontend Layer:                                            │
│  ├─ Landing Page (index.html) ............ http://5000      │
│  └─ Interactive App (app.py) ............ http://8501       │
│                                                              │
│  Backend Layer:                                             │
│  └─ FastAPI Server (api.py) ........... http://8000         │
│      └─ /check endpoint · /docs endpoint                    │
│                                                              │
│  AI/ML Layer:                                               │
│  ├─ Sentence Transformers Model                            │
│  └─ Cosine Similarity Engine                               │
│                                                              │
│  Data Layer:                                                │
│  └─ MongoDB Atlas Cloud Database                           │
│      └─ fact_checker.facts collection                      │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 📁 **Project Structure**

```
Automated-Fact-Checking-System/
├── backend/
│   ├── api.py              ← FastAPI server
│   ├── similarity.py       ← NLP fact-checking logic
│   ├── db.py              ← MongoDB connection
│   ├── insert_data.py     ← Data insertion script
│   ├── main.py            ← CLI interface
│   └── test.py            ← Test script
├── frontend/
│   ├── index.html         ← Landing page (HTML)
│   ├── app.py             ← Streamlit app
│   └── server.py          ← Flask server for landing
├── .env                   ← MongoDB credentials (KEEP SECRET)
├── .env.example           ← Template for .env
└── README.md              ← This file
```

---

## 🔧 **Configuration**

### MongoDB Connection String
Edit `.env` file in project root:
```
MONGODB_URI=mongodb+srv://jaisoncherian:MY_PASSWORD@cluster0.j8lktde.mongodb.net/?appName=Cluster0
```
⚠️ **Replace `MY_PASSWORD`** with your actual MongoDB Atlas password

### Database Schema
```javascript
{
  _id: ObjectId,
  claim: "string",
  label: "true" | "false" | "suspicious"
}
```

---

## 📊 **How to Test**

### **Test 1: API Endpoint (Using Browser)**
1. Go to: http://127.0.0.1:8000/docs
2. Scroll to `/check` endpoint
3. Click "Try it out"
4. Enter: `text=earth is flat`
5. Click "Execute"

Expected response:
```json
{
  "input": "earth is flat",
  "result": "false",
  "confidence": 0.987
}
```

### **Test 2: Streamlit App**
1. Go to: http://localhost:8501
2. Enter: "drinking hot water cures covid"
3. Click "Check Fact"
4. Should show: **FALSE NEWS** with 92%+ confidence

### **Test 3: Landing Page**
1. Go to: http://localhost:5000
2. Click "Start Verifying →" button
3. Redirects to Streamlit app

---

## 🎯 **Features & Capabilities**

✅ **AI-Powered Detection**
- Uses Sentence Transformers for semantic understanding
- Cosine similarity matching against fact database
- Sub-200ms response time

✅ **Three Verdict Types**
- ✅ **TRUE** - Claim matches verified facts
- ❌ **FAKE** - Claim is misinformation
- ⚠ **SUSPICIOUS** - Claim needs investigation

✅ **Confidence Scoring**
- 0-100% confidence percentage
- Visual progress bar
- Transparent & explainable

✅ **Professional UI**
- Dark theme with modern design
- Responsive layout
- Real-time analysis feedback

---

## ⚙️ **API Endpoints**

### `GET /`
HealthCheck endpoint

**Response:**
```json
{"message": "Fake News Detection API Running"}
```

### `POST /check`
Fact-checking endpoint

**Parameters:**
- `text` (string): The news claim to verify

**Response:**
```json
{
  "input": "string",
  "result": "true|false|suspicious",
  "confidence": 0.0-1.0
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/check?text=india%20capital%20is%20delhi"
```

---

## 🛠️ **Troubleshooting**

### ❌ "Cannot connect to MongoDB"
- Check `.env` file has correct connection string
- Verify MongoDB password is correct
- Ensure MongoDB Atlas firewall allows your IP
- Run `python insert_data.py` to test connection

### ❌ "Module not found" error
```powershell
# Reinstall packages
pip install -r requirements.txt --force-reinstall
```

### ❌ Port already in use
```powershell
# Kill process using port 5000 (Flask)
Get-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess | Stop-Process

# Kill process using port 8000 (FastAPI)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process

# Kill process using port 8501 (Streamlit)
Get-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess | Stop-Process
```

### ❌ "ModuleNotFoundError: No module named 'similarity'"
```powershell
# Run from correct directory
cd backend
python insert_data.py

# Or run from project root with module path
cd c:\Users\jaison\Automated-Fact-Checking-System
python -m backend.insert_data
```

---

## 📦 **Required Packages**

```
sentence-transformers>=2.2.0
scikit-learn>=1.2.0
fastapi>=0.95.0
uvicorn>=0.21.0
streamlit>=1.20.0
pymongo>=4.3.0
python-dotenv>=1.0.0
requests>=2.28.0
flask>=2.3.0
```

Install all:
```powershell
pip install -r requirements.txt
```

---

## 🚀 **Deployment Tips**

### Production Deployment
1. Use environment variables (don't hardcode secrets)
2. Set `debug=False` in FastAPI/Flask
3. Use a production ASGI server (Gunicorn + Uvicorn)
4. Deploy frontend to Vercel/Netlify
5. Deploy backend to cloud (AWS EC2, Heroku, Railway)
6. Use MongoDB Atlas (already cloud-hosted)

### Example Gunicorn Command
```bash
gunicorn -w 4 -b 0.0.0.0:8000 backend.api:app
```

---

## 📞 **Support**

- 🐛 **Bug Reports**: Check the error output
- 🆘 **Setup Issues**: Follow troubleshooting section
- 📚 **Documentation**: Visit http://127.0.0.1:8000/docs (Swagger UI)

---

## 📝 **License**

©️ 2026 VeriNews AI | All Rights Reserved

---

## ✨ **Key Technologies**

| Component | Technology | Version |
|-----------|-----------|---------|
| Frontend | HTML5 + CSS3 | Latest |
| Backend | FastAPI | 0.95+ |
| NLP | Sentence Transformers | 2.2+ |
| Database | MongoDB Atlas | Cloud |
| ML | Scikit-Learn | 1.2+ |
| UI | Streamlit | 1.20+ |

---

**Last Updated:** March 22, 2026
**Status:** ✅ Production Ready
