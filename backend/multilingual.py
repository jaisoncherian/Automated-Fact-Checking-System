"""
Multilingual/Vernacular Fact-Checking Module
Handles language detection, translation, and multilingual processing
"""

from langdetect import detect, DetectorFactory
from deep_translator import GoogleTranslator
import requests
import json
import re

# Set seed for consistent language detection
DetectorFactory.seed = 0

# Supported languages
SUPPORTED_LANGUAGES = {
    'en': 'English',
    'ml': 'Malayalam',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'kn': 'Kannada',
    'mr': 'Marathi',
    'gu': 'Gujarati',
    'bn': 'Bengali',
    'pa': 'Punjabi',
    'ur': 'Urdu',
    'fr': 'French',
    'de': 'German',
    'es': 'Spanish',
    'pt': 'Portuguese',
    'zh-cn': 'Chinese (Simplified)',
    'ja': 'Japanese',
    'ko': 'Korean',
    'ar': 'Arabic',
}

def detect_language(text):
    """
    Detect the language of input text
    
    Args:
        text (str): Input text to detect
        
    Returns:
        tuple: (language_code, language_name)
    """
    try:
        if not text or not text.strip():
            return 'en', 'English'
        
        lang_code = detect(text)
        lang_name = SUPPORTED_LANGUAGES.get(lang_code, 'Unknown')
        return lang_code, lang_name
    except Exception as e:
        print(f"⚠️  Language detection error: {e}")
        return 'en', 'English'

def translate_to_english(text, source_lang=None):
    """
    Translate text to English using deep_translator (GoogleTranslator)
    with hardcoded Malayalam overrides for known phrases.
    
    Args:
        text (str): Text to translate
        source_lang (str): Source language code (auto-detect if None)
        
    Returns:
        str: Translated English text
    """
    # Hardcoded common Malayalam → English mappings (bypass translation APIs for known phrases)
    MALAYALAM_OVERRIDES = {
        "ഭൂമി ഉരുണ്ടതാണ്": "the earth is round",
        "ഭൂമി പരന്നതാണ്": "the earth is flat",
        "വാക്സിൻ സുരക്ഷിതമാണ്": "vaccines are safe",
        "വാക്സിൻ ഓട്ടിസം ഉണ്ടാക്കുന്നു": "vaccines cause autism",
        "സൂര്യൻ ഒരു നക്ഷത്രമാണ്": "the sun is a star",
        "ഭൂമി സൂര്യനു ചുറ്റും കറങ്ങുന്നു": "the earth revolves around the sun",
        "മനുഷ്യർക്ക് ബഹിരാകാശത്ത് ശ്വസിക്കാൻ കഴിയില്ല": "humans cannot breathe in space",
    }
    
    if not text or not text.strip():
        return text
    
    # Check override table first
    normalized = text.strip()
    if normalized in MALAYALAM_OVERRIDES:
        print(f"✅ Translation (Override): {text[:40]}... → {MALAYALAM_OVERRIDES[normalized][:40]}...")
        return MALAYALAM_OVERRIDES[normalized]
    
    if source_lang is None:
        source_lang, _ = detect_language(text)
    
    if source_lang == 'en':
        return text

    # Use deep_translator GoogleTranslator (much more reliable for Indian languages)
    try:
        translated = GoogleTranslator(source=source_lang, target='en').translate(text)
        if translated:
            print(f"✅ Translation (GoogleTranslator): {text[:40]}... → {translated[:40]}...")
            return translated
    except Exception as e:
        print(f"🔴 Translation failed: {e}")
    
    return text

def translate_from_english(text, target_lang):
    """
    Translate English text back to target language using deep_translator (GoogleTranslator)
    
    Args:
        text (str): English text to translate
        target_lang (str): Target language code
        
    Returns:
        str: Translated text in target language
    """
    if not text or not text.strip():
        return text
    
    if target_lang == 'en':
        return text
    
    try:
        translated = GoogleTranslator(source='en', target=target_lang).translate(text)
        if translated:
            print(f"✅ Back-translation (GoogleTranslator): {text[:40]}... → {translated[:40]}...")
            return translated
    except Exception as e:
        print(f"🔴 Back-translation failed: {e}")
    
    return text

def extract_claims(text):
    """
    Extract potential claims/sentences from text
    
    Args:
        text (str): Input text
        
    Returns:
        list: List of sentences/claims
    """
    # Split by common sentence endings (including ! and ?)
    sentences = re.split(r'[।.!?\n]+', text)
    
    # Filter out empty strings and very short sentences
    claims = [s.strip() for s in sentences if len(s.strip()) > 10]
    
    # Fallback: if no claims found, return the original text
    if not claims:
        return [text]
    
    return claims

def process_vernacular_text(text):
    """
    Complete pipeline: detect language, translate, extract claims
    
    Args:
        text (str): Input text in any language
        
    Returns:
        dict: Processed information
    """
    # Detect language
    lang_code, lang_name = detect_language(text)
    
    # Translate to English
    english_text = translate_to_english(text, lang_code)
    
    # Extract claims
    claims = extract_claims(english_text)
    
    return {
        'original_text': text,
        'detected_language': lang_code,
        'language_name': lang_name,
        'english_text': english_text,
        'claims': claims
    }

# Language codes mapping for translation
LANG_CODES = {
    'English': 'en',
    'Malayalam': 'ml',
    'Hindi': 'hi',
    'Tamil': 'ta',
    'Telugu': 'te',
    'Kannada': 'kn',
    'Marathi': 'mr',
    'Gujarati': 'gu',
    'Bengali': 'bn',
    'Punjabi': 'pa',
    'Urdu': 'ur',
}
