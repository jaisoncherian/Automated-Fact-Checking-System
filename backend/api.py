import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from similarity import check_fact

app = FastAPI()

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Fake News Detection API Running"}

@app.post("/check")
def check_news(text: str):
    result, score = check_fact(text)

    # Whitelist - never let an unexpected value reach the frontend
    ALLOWED = {"true", "false", "suspicious", "unknown"}
    result = result.lower().strip()
    if result not in ALLOWED:
        result = "unknown"

    return {
        "input": text,
        "result": result,
        "confidence": round(float(score), 4)
    }
