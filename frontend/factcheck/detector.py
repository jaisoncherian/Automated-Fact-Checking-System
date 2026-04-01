"""
Language detection module for factcheck.
Uses langdetect to identify the language of input text.
"""

from langdetect import detect, DetectorFactory

# Set seed for consistent results
DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """
    Detect the language of input text.
    
    Args:
        text (str): Input text to detect
        
    Returns:
        str: ISO 639-1 language code (e.g., "ml", "hi", "en")
    """
    try:
        if not text or not text.strip():
            return "en"
        
        lang_code = detect(text)
        return lang_code
    except Exception as e:
        print(f"⚠️  Language detection error: {e}")
        return "en"
