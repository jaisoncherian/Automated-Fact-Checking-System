import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from similarity import check_fact

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NewsText(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Fake News Detection API Running"}

@app.post("/check")
def check_news(news: NewsText):
    try:
        if not news.text or not news.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        result, score = check_fact(news.text)

        # Whitelist - only allow these three verdicts
        ALLOWED = {"true", "fake", "suspicious"}
        result = result.lower().strip()
        # Clean: remove ALL whitespace
        result = ''.join(result.split())
        if result not in ALLOWED:
            result = "suspicious"  # Fallback to suspicious if somehow invalid

        return {
            "input": news.text,
            "result": result,
            "confidence": round(float(score), 4)
        }
    except Exception as e:
        print(f"ERROR in check_news: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

