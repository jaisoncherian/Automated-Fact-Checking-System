"""
Claim extraction module for factcheck.
Extracts check-worthy factual sentences from English text using spacy.
"""

import spacy

# Load spacy model at module level
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise RuntimeError("Run: python -m spacy download en_core_web_sm")


def extract_claims(text: str) -> list:
    """
    Extract check-worthy factual sentences from English text.
    
    Processing rules:
    - Skip sentences shorter than 20 characters
    - Skip questions (ending with "?")
    - Skip sentences without verbs
    - Return fallback [text] if no claims found
    
    Args:
        text (str): English text to extract claims from
        
    Returns:
        list[str]: List of extracted claims/sentences
    """
    try:
        doc = nlp(text)
        claims = []
        
        for sentence in doc.sents:
            sentence_text = sentence.text.strip()
            
            # Skip short sentences
            if len(sentence_text) < 20:
                continue
            
            # Skip questions
            if sentence_text.endswith("?"):
                continue
            
            # Skip sentences without verbs
            has_verb = any(token.pos_ == "VERB" for token in sentence)
            if not has_verb:
                continue
            
            claims.append(sentence_text)
        
        # Return fallback if no claims extracted
        if not claims:
            return [text]
        
        return claims
    except Exception as e:
        print(f"⚠️  Claim extraction error: {e}")
        return [text]
