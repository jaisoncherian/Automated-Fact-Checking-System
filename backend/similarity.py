from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from db import collection

model = SentenceTransformer('all-MiniLM-L6-v2')

# Valid labels accepted from DB
VALID_LABELS = {"true", "false"}

def check_fact(user_input):
    """Check a claim against known facts using similarity thresholds."""
    
    print(f"\n{'='*60}")
    print(f"🔍 INPUT: {user_input}")

    facts = list(collection.find())
    print(f"📊 Total facts in DB: {len(facts)}")

    if not facts:
        print("❌ No facts in DB!")
        return "unknown", 0.0

    claims = [fact["claim"] for fact in facts]
    embeddings = model.encode([user_input] + claims)

    user_vec = embeddings[0]
    fact_vecs = embeddings[1:]

    scores = cosine_similarity([user_vec], fact_vecs)[0]

    max_score = float(max(scores))
    index = scores.tolist().index(max_score)
    matched_fact = facts[index]

    raw_label = str(matched_fact.get("label", "")).lower().strip()

    print(f"🎯 Best match : {matched_fact['claim']}")
    print(f"📈 Score      : {max_score:.4f}")
    print(f"🏷️  DB label   : {raw_label}")

    # ── Threshold logic ──────────────────────────────────────
    if max_score >= 0.75:
        # Strong match — trust the DB label only if it's valid
        if raw_label in VALID_LABELS:
            result = raw_label
            print(f"✅ Strong match → '{result}'")
        else:
            # DB has a bad/missing label — treat as unknown
            result = "unknown"
            print(f"⚠️  Strong match but invalid DB label '{raw_label}' → 'unknown'")

    elif max_score >= 0.5:
        result = "suspicious"
        print(f"⚠️  Weak match (0.5–0.75) → 'suspicious'")

    else:
        result = "unknown"
        print(f"❌ No match (< 0.5) → 'unknown'")

    print(f"📤 FINAL: {result} | score: {max_score:.4f}")
    print(f"{'='*60}\n")

    return result, max_score


