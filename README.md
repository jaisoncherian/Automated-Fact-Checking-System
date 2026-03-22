# VeriNews AI – Automated Fact-Checking System

A production-grade AI-powered fact-checking system that verifies news claims in real-time using semantic embeddings and cosine similarity matching against a trusted facts database.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
- [Screenshots](#screenshots)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

## Overview

VeriNews AI is an intelligent fact-checking system that detects misinformation in news claims and social media content. Instead of keyword matching, it uses advanced NLP techniques to understand semantic meaning and match user input against thousands of verified facts. 

**Problem Solved:** Misinformation spreads faster than corrections. VeriNews AI provides instant, confidence-scored verdicts on claim authenticity.

**Target Users:** Journalists, content moderators, fact-checking organizations, and misinformation researchers.

**Core Technology:** Leverages Sentence Transformers for semantic embeddings combined with cosine similarity to find the most relevant matching fact in milliseconds.

## Features

- **AI-Based Semantic Matching** – Uses state-of-the-art Sentence Transformers (all-MiniLM-L6-v2) for understanding claim meaning beyond keywords
- **Real-Time Analysis** – Returns verdict with confidence score in <200ms
- **Three Verdict Types** – Clear, actionable outputs: **TRUE**, **FAKE**, or **SUSPICIOUS**
- **Confidence Scoring** – Every verdict includes a 0-100% confidence percentage
- **Multilingual Support** – Processes claims across 12+ languages
- **REST API** – Clean, documented FastAPI endpoint for easy integration
- **Web Interface** – Interactive demo card with live fact-checking
- **Cloud Database** – MongoDB Atlas integration with fallback to mock data
- **Production Ready** – CORS enabled, error handling, graceful degradation

## Tech Stack

- **Frontend:** 
  - Flask (Python) for serving static HTML
  - HTML5/CSS3/JavaScript (vanilla)
  - Responsive design with Tailwind CSS
  
- **Backend:** 
  - FastAPI (Python) – High-performance REST API
  - Sentence Transformers – NLP embeddings
  - scikit-learn – Cosine similarity computation
  
- **Database:** 
  - MongoDB Atlas (cloud) – Primary fact store
  - Mock Data Fallback – 50+ verified facts for offline use
  
- **Tools/Platforms:** 
  - Git/GitHub – Version control
  - Python 3.9+ with virtual environment
  - uvicorn – ASGI server

## Installation

### Prerequisites
- Python 3.9 or higher
- Git
- MongoDB Atlas account (optional – uses mock data if unavailable)

### Clone the Repository
```bash
git clone https://github.com/jaisoncherian/Automated-Fact-Checking-System.git
cd Automated-Fact-Checking-System
```

### Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure Database (Optional)
If using MongoDB Atlas, update your connection string in `backend/db.py`:
```python
MONGO_URI = "your-mongodb-atlas-connection-string"
```

## Usage

### Start the Backend Server
```bash
cd backend
uvicorn api:app --host 127.0.0.1 --port 8000 --reload
```

Backend will be available at `http://127.0.0.1:8000`

### Start the Frontend Server
```bash
cd frontend
python server.py
```

Frontend will be available at `http://localhost:5000`

### Test a Claim
1. Open `http://localhost:5000` in your browser
2. Enter a news claim (e.g., "earth is flat")
3. Click "Analyze Claim"
4. View the verdict and confidence score

### Using the API Directly
```bash
curl -X POST http://127.0.0.1:8000/check \
  -H "Content-Type: application/json" \
  -d '{"text": "vaccines cause autism"}'
```

Response:
```json
{
  "input": "vaccines cause autism",
  "result": "fake",
  "confidence": 0.9772
}
```

## Project Structure

```
Automated-Fact-Checking-System/
├── backend/
│   ├── api.py                 # FastAPI application & /check endpoint
│   ├── similarity.py          # Core fact-checking logic with NLP
│   ├── db.py                  # MongoDB connection management
│   ├── insert_data.py         # Sample data insertion script
│   └── __pycache__/
├── frontend/
│   ├── index.html             # Main web interface (HTML/CSS/JS)
│   ├── server.py              # Flask server
│   ├── public/                # Static assets
│   └── src/                   # Frontend source (React setup available)
├── venv/                      # Virtual environment
├── requirements.txt           # Python dependencies
├── README.md                  # This file
├── DEPLOYMENT_GUIDE.md        # Production deployment instructions
└── .git/                      # Git repository
```

## API Endpoints

### POST /check
**Check a claim and get a verdict**

**Request:**
```json
{
  "text": "The Earth is flat"
}
```

**Response (200 OK):**
```json
{
  "input": "The Earth is flat",
  "result": "fake",
  "confidence": 0.9873
}
```

**Verdict Types:**
- `"true"` – Claim matches a verified true fact (confidence ≥ 0.40)
- `"fake"` – Claim matches a known false claim (confidence ≥ 0.40)
- `"suspicious"` – Weak match or insufficient confidence to determine

**Error Response (400):**
```json
{"detail": "Text cannot be empty"}
```

### GET /
**Health check**

Returns: `{"message": "Fake News Detection API Running"}`

### GET /docs
**Interactive API documentation** (Swagger UI)

Available at `http://127.0.0.1:8000/docs`

## Screenshots

### Web Interface
The interactive demo card allows users to:
- Enter a news claim
- See real-time verdict with confidence percentage
- View color-coded verdict badges (✓ TRUE, ✗ FAKE, ⚠ SUSPICIOUS)

### Console Debugging
Real-time backend logs show:
```
🎯 Best match : Vaccines cause autism
📈 Score      : 0.9772
🏷️  DB label   : 'false' (cleaned)
✅ Match → 'fake'
📤 FINAL: fake | score: 0.9772
```

## Verdict Logic

| Score Range | Result | Description |
|------------|--------|-------------|
| ≥ 0.40 | TRUE/FAKE | Strong match – trust the label |
| 0.25–0.40 | SUSPICIOUS | Weak match – uncertain |
| < 0.25 | SUSPICIOUS | No match found – default safe |

## Future Enhancements

- [ ] **Source Attribution** – Show which fact database entry matched
- [ ] **Explanation Generation** – Provide reasoning for verdict ("Why this claim is marked as FAKE")
- [ ] **User Feedback Loop** – Allow users to flag incorrect verdicts for model retraining
- [ ] **Batch Processing** – Support checking multiple claims simultaneously
- [ ] **Fact Database Editor** – Admin panel to add/edit/remove claims
- [ ] **Mobile App** – iOS/Android native applications
- [ ] **Browser Extension** – Real-time fact-checking while browsing web
- [ ] **Claim Source Tracking** – Monitor which claims go viral and when
- [ ] **Multi-Language Output** – Return verdicts in user's language
- [ ] **Fine-tuned Models** – Domain-specific (health, politics, science)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add feature description'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License – see the LICENSE file for details.

## Author

**Jaison Cherian**
- GitHub: [@jaisoncherian](https://github.com/jaisoncherian)
- Project: [Automated-Fact-Checking-System](https://github.com/jaisoncherian/Automated-Fact-Checking-System)

---

## Quick Start Summary

```bash
# 1. Clone and setup
git clone https://github.com/jaisoncherian/Automated-Fact-Checking-System.git
cd Automated-Fact-Checking-System
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt

# 2. Start backend
cd backend
uvicorn api:app --host 127.0.0.1 --port 8000 --reload

# 3. (New terminal) Start frontend
cd frontend
python server.py

# 4. Open browser
# http://localhost:5000
```

**Status:** ✅ Fully Functional | Ready for Production | Mock Data Fallback Active