"""
Translation module for factcheck.
Translates text to English and back to original language.
Uses the existing googletrans library.
"""

import requests


def translate_to_english(text: str, source_lang: str) -> str:
    """
    Translate text to English using MyMemory API.
    
    Args:
        text (str): Text to translate
        source_lang (str): ISO 639-1 language code of source language
        
    Returns:
        str: Translated English text, or original if translation fails
    """
    try:
        if source_lang == "en":
            return text
        
        # Try MyMemory API first (reliable)
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'{source_lang}|en'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated and translated != text:
                    return translated
        
        # Fallback to Google Translate
        url = "https://translate.googleapis.com/translate_a/element.js"
        params = {
            'client': 'gtx',
            'sl': source_lang,
            'tl': 'en',
            'text': text
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            content = response.text
            if ',["' in content:
                parts = content.split(',["')
                if len(parts) > 1:
                    translated = parts[1].split('","')[0]
                    if translated and len(translated) > 2:
                        return translated
        
        return text
    except Exception as e:
        print(f"⚠️  Translation to English error: {e}")
        return text


def translate_back(text: str, target_lang: str) -> str:
    """
    Translate English text back to target language.
    
    Args:
        text (str): English text to translate
        target_lang (str): ISO 639-1 language code of target language
        
    Returns:
        str: Translated text, or original if translation fails
    """
    try:
        if target_lang == "en":
            return text
        
        # Try MyMemory API first (reliable)
        url = "https://api.mymemory.translated.net/get"
        params = {
            'q': text,
            'langpair': f'en|{target_lang}'
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('responseStatus') == 200:
                translated = data.get('responseData', {}).get('translatedText', '')
                if translated and translated != text:
                    return translated
        
        # Fallback to Google Translate
        url = "https://translate.googleapis.com/translate_a/element.js"
        params = {
            'client': 'gtx',
            'sl': 'en',
            'tl': target_lang,
            'text': text
        }
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            content = response.text
            if ',["' in content:
                parts = content.split(',["')
                if len(parts) > 1:
                    translated = parts[1].split('","')[0]
                    if translated and len(translated) > 2:
                        return translated
        
        return text
    except Exception as e:
        print(f"⚠️  Translation back error: {e}")
        return text

