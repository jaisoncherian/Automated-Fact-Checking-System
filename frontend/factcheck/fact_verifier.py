"""
Fact verification module for factcheck.
Compares claims against MongoDB facts using semantic similarity.
"""

import os
from sentence_transformers import SentenceTransformer, util

# Load model at module level (runs once on import)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load knowledge base from MongoDB
def load_knowledge_base() -> list:
    """
    Load the knowledge base from MongoDB.
    
    Returns:
        list: List of fact dictionaries with keys: claim, label/verdict
    """
    try:
        # Try to connect to MongoDB
        from pymongo import MongoClient
        import os
        
        mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017/verinews")
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        db = client.verinews
        collection = db.facts
        
        # Get all facts from MongoDB
        facts = list(collection.find({}, {"_id": 0}))
        
        if not facts:
            print("⚠️  No facts found in MongoDB, using fallback facts")
            return get_fallback_facts()
        
        return facts
    except Exception as e:
        print(f"⚠️  MongoDB connection failed: {e}")
        print("   Using fallback facts instead")
        return get_fallback_facts()


def get_fallback_facts() -> list:
    """
    Fallback facts if MongoDB is unavailable.
    
    Returns:
        list: List of fallback fact dictionaries
    """
    return [
        {"claim": "Earth is flat", "label": "false"},
        {"claim": "Vaccines cause autism", "label": "false"},
        {"claim": "India is in Asia", "label": "true"},
        {"claim": "The sun is a star", "label": "true"},
        {"claim": "Humans can breathe in space without equipment", "label": "false"},
        {"claim": "Water boils at 100 degrees celsius", "label": "true"},
        {"claim": "The earth revolves around the sun", "label": "true"},
        {"claim": "Light travels faster than sound", "label": "true"},
        {"claim": "AI will replace all human jobs", "label": "false"},
        {"claim": "COVID-19 vaccines contain microchips", "label": "false"},
    ]


# Load knowledge base at module level
knowledge_base = load_knowledge_base()

# Encode all claims from knowledge base
kb_claims = [fact.get("claim", "") for fact in knowledge_base]
kb_embeddings = model.encode(kb_claims, convert_to_tensor=True)


def verify_claims(claims: list) -> list:
    """
    Verify claims against MongoDB facts using semantic similarity.
    
    For each claim:
    - Encode it with the sentence transformer model
    - Compute cosine similarity against all knowledge base claims
    - If best match score >= 0.45, use that fact's verdict
    - Otherwise, mark as "Unverified"
    
    Args:
        claims (list[str]): List of claims to verify
        
    Returns:
        list[dict]: List of results with keys: claim, verdict, explanation, confidence
    """
    results = []
    
    for claim in claims:
        try:
            # Encode the claim
            claim_embedding = model.encode(claim, convert_to_tensor=True)
            
            # Compute similarity scores
            scores = util.cos_sim(claim_embedding, kb_embeddings)[0]
            
            # Find best match
            best_idx = int(scores.argmax())
            best_score = float(scores[best_idx])
            
            # Determine verdict based on score threshold
            if best_score >= 0.45:
                fact = knowledge_base[best_idx]
                # Convert label to verdict format
                label = fact.get("label", "").lower()
                verdict = "True" if label == "true" else "False" if label == "false" else "Unverified"
                explanation = f"This claim matches: '{fact.get('claim', '')}' in the knowledge base."
            else:
                verdict = "Unverified"
                explanation = "No matching fact found in the knowledge base. Please consult a trusted source."
            
            # Build result
            result = {
                "claim": claim,
                "verdict": verdict,
                "explanation": explanation,
                "confidence": round(best_score * 100, 1)
            }
            results.append(result)
            
        except Exception as e:
            print(f"⚠️  Error verifying claim '{claim}': {e}")
            results.append({
                "claim": claim,
                "verdict": "Error",
                "explanation": "An error occurred while verifying this claim.",
                "confidence": 0.0
            })
    
    return results

