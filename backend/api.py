import sys
from pathlib import Path

# Add backend directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from similarity import check_fact
from multilingual import (
    detect_language,
    translate_to_english,
    translate_from_english,
    extract_claims,
    process_vernacular_text,
    SUPPORTED_LANGUAGES
)

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
    language: str = None  # Optional: user can specify language

@app.get("/")
def home():
    return {
        "message": "Automated Vernacular Fact-Checking API",
        "version": "2.0",
        "endpoints": {
            "/check": "Check news in any language (auto-translates to English)",
            "/check-multilingual": "Check news in any language (Malayalam, Hindi, Tamil, etc.) with per-claim results",
            "/supported-languages": "Get list of supported languages"
        }
    }

@app.post("/check")
def check_news(news: NewsText):
    try:
        if not news.text or not news.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")
        
        # Detect language and translate to English if needed
        detected_lang, _ = detect_language(news.text)
        english_text = translate_to_english(news.text, detected_lang)
        
        result, score, _ = check_fact(english_text)

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

@app.post("/check-multilingual")
def check_news_multilingual(news: NewsText):
    """
    Check news/claims in any language (vernacular fact-checking)
    
    Features:
    - Auto-detects input language
    - Translates to English for processing
    - Extracts individual claims from the text
    - Returns per-claim results with explanations in original language
    
    Example:
    {
        "text": "AI എല്ലാം ജോലികൾ മാറ്റും [Malayalam: AI will replace all jobs]",
        "language": "ml"  # Optional
    }
    """
    try:
        if not news.text or not news.text.strip():
            raise HTTPException(status_code=400, detail="Text cannot be empty")

        # Step 1: Detect language
        detected_lang, lang_name = detect_language(news.text)

        # Step 2: Translate full input to English
        english_text = translate_to_english(news.text, detected_lang)

        # Step 3: Extract individual claims from English text
        claims = extract_claims(english_text)

        # Step 4: Check each claim and build results
        per_claim_results = []
        for claim in claims:
            verdict, confidence, explanation_en = check_fact(claim)

            # Step 5: Translate explanation back to original language
            explanation_local = translate_from_english(explanation_en, detected_lang)

            per_claim_results.append({
                "claim": claim,
                "verdict": verdict,
                "confidence": round(float(confidence), 4),
                "explanation": explanation_local
            })

        return {
            "original_text": news.text,
            "english_translation": english_text,
            "detected_language": detected_lang,
            "language_name": lang_name,
            "claims_found": len(claims),
            "results": per_claim_results
        }

    except Exception as e:
        print(f"ERROR in check_news_multilingual: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/supported-languages")
def get_supported_languages():
    """Get list of all supported languages"""
    return {
        "supported_languages": SUPPORTED_LANGUAGES,
        "total_languages": len(SUPPORTED_LANGUAGES),
        "note": "Use language codes (e.g., 'ml' for Malayalam) when specifying language"
    }

