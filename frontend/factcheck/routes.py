"""
Flask Blueprint for factcheck API endpoint.
Provides POST /factcheck/check for vernacular fact-checking.
"""

from flask import Blueprint, request, jsonify

from factcheck.detector import detect_language
from factcheck.translator import translate_to_english, translate_back
from factcheck.claim_extractor import extract_claims
from factcheck.fact_verifier import verify_claims

# Create Blueprint
factcheck_bp = Blueprint("factcheck", __name__, url_prefix="/factcheck")


@factcheck_bp.route("/check", methods=["POST"])
def check_facts():
    """
    POST /factcheck/check
    
    Accepts JSON with "text" field in any language.
    Returns fact-checking results for extracted claims.
    
    Flow:
    1. Detect language
    2. Translate to English
    3. Extract claims
    4. Verify claims
    5. Translate explanations back to original language
    6. Return results
    """
    try:
        # Parse JSON body
        data = request.get_json()
        
        # Get text
        text = data.get("text", "").strip()
        if not text:
            return jsonify({"error": "No text provided"}), 400
        
        # Step 1: Detect language
        lang = detect_language(text)
        
        # Step 2: Translate to English
        english_text = translate_to_english(text, lang)
        
        # Step 3: Extract claims
        claims = extract_claims(english_text)
        
        # Step 4: Verify claims
        raw_results = verify_claims(claims)
        
        # Step 5: Translate results back to original language
        translated_results = []
        for r in raw_results:
            translated_results.append({
                "original_claim": r["claim"],
                "verdict": r["verdict"],
                "explanation": translate_back(r["explanation"], lang),
                "confidence": r["confidence"]
            })
        
        # Step 6: Return results
        return jsonify({
            "detected_language": lang,
            "claims_found": len(claims),
            "results": translated_results
        }), 200
        
    except Exception as e:
        print(f"❌ Error in /factcheck/check: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
