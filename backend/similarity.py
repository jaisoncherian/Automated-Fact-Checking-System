from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Try to import from db
try:
    from db import collection
    HAS_DB = collection is not None
except:
    HAS_DB = False
    collection = None

model = SentenceTransformer('all-MiniLM-L6-v2')

# Valid labels accepted from DB
VALID_LABELS = {"true", "false"}

# Mock data for testing when MongoDB is unavailable
MOCK_FACTS = [
    # SCIENCE - TRUE
    {"claim": "The Earth is round", "label": "true"},
    {"claim": "The Earth is spherical", "label": "true"},
    {"claim": "Water boils at 100 degrees Celsius", "label": "true"},
    {"claim": "Climate change is real", "label": "true"},
    {"claim": "Humans need oxygen to survive", "label": "true"},
    {"claim": "The sun is a star", "label": "true"},
    {"claim": "Fish live in water", "label": "true"},
    {"claim": "Fish need water to survive", "label": "true"},
    {"claim": "The moon orbits the Earth", "label": "true"},
    {"claim": "The moon is a natural satellite", "label": "true"},
    {"claim": "Plants need sunlight to grow", "label": "true"},
    {"claim": "Humans have 206 bones", "label": "true"},
    {"claim": "Light travels faster than sound", "label": "true"},
    {"claim": "The Earth orbits the Sun", "label": "true"},
    {"claim": "DNA carries genetic information", "label": "true"},
    {"claim": "Gravity pulls objects toward Earth", "label": "true"},

    # SCIENCE - FALSE
    {"claim": "The Earth is flat", "label": "false"},
    {"claim": "The moon is a planet", "label": "false"},
    {"claim": "The moon is made of cheese", "label": "false"},
    {"claim": "Fish can live without water", "label": "false"},
    {"claim": "Fish can survive without water", "label": "false"},
    {"claim": "Humans can breathe underwater without equipment", "label": "false"},
    {"claim": "The sun revolves around the Earth", "label": "false"},
    {"claim": "Plants do not need sunlight", "label": "false"},
    {"claim": "Humans only use 10 percent of their brain", "label": "false"},
    {"claim": "Lightning never strikes the same place twice", "label": "false"},
    {"claim": "Goldfish have a 3 second memory", "label": "false"},

    # HEALTH - TRUE
    {"claim": "Vaccines are safe and effective", "label": "true"},
    {"claim": "Exercise is good for health", "label": "true"},
    {"claim": "Smoking causes cancer", "label": "true"},
    {"claim": "Drinking water is essential for survival", "label": "true"},

    # HEALTH - FALSE
    {"claim": "Vaccines cause autism", "label": "false"},
    {"claim": "5G causes COVID-19", "label": "false"},
    {"claim": "Drinking bleach cures diseases", "label": "false"},
    {"claim": "Antibiotics cure viral infections", "label": "false"},

    # SPACE - TRUE
    {"claim": "Mars is a planet", "label": "true"},
    {"claim": "There are eight planets in the solar system", "label": "true"},
    {"claim": "Saturn has rings", "label": "true"},
    {"claim": "Pluto is a dwarf planet", "label": "true"},

    # SPACE - FALSE
    {"claim": "Pluto is a full planet", "label": "false"},
    {"claim": "The moon is a planet", "label": "false"},
    {"claim": "Stars are holes in the sky", "label": "false"},
    {"claim": "The sun is cold", "label": "false"},
]

def check_fact(user_input):
    """Check a claim against known facts using similarity thresholds."""
    
    print(f"\n{'='*60}")
    print(f"🔍 INPUT: {user_input}")

    # Get facts from DB or use mock data
    facts = []
    if HAS_DB and collection:
        try:
            facts = list(collection.find())
            print("✅ Using database facts")
        except Exception as e:
            print(f"⚠️  Database query failed: {e}")
            facts = MOCK_FACTS
            print("⚠️  Falling back to MOCK DATA")
    else:
        facts = MOCK_FACTS
        print("⚠️  Using MOCK DATA (MongoDB unavailable)")
    
    print(f"📊 Total facts: {len(facts)}")

    if not facts:
        print("❌ No facts in DB!")
        return "suspicious", 0.0

    claims = [fact["claim"] for fact in facts]
    embeddings = model.encode([user_input] + claims)

    user_vec = embeddings[0]
    fact_vecs = embeddings[1:]

    scores = cosine_similarity([user_vec], fact_vecs)[0]

    max_score = float(max(scores))
    index = scores.tolist().index(max_score)
    matched_fact = facts[index]

    # Extract and AGGRESSIVELY clean the label (remove ALL whitespace/special chars)
    raw_label = str(matched_fact.get("label", "")).lower().strip()
    # Remove ALL whitespace including \n, \r, \t, spaces, etc.
    raw_label = ''.join(raw_label.split())
    
    print(f"🎯 Best match : {matched_fact['claim']}")
    print(f"📈 Score      : {max_score:.4f}")
    print(f"🏷️  DB label   : '{raw_label}' (cleaned)")

    # ── Threshold logic ──────────────────────────────────────
    if max_score >= 0.40:          # lowered from 0.60
        # Good match — trust the label directly
        if raw_label == "true":
            result = "true"
            print(f"✅ Match → 'true'")
        elif raw_label == "false":
            result = "fake"
            print(f"✅ Match → 'fake'")
        else:
            result = "suspicious"
            print(f"⚠️  Invalid label → 'suspicious'")
    elif max_score >= 0.25:
        # Weak match
        result = "suspicious"
        print(f"⚠️  Weak match → 'suspicious'")
    else:
        # Very weak — unknown
        result = "unknown"
        print(f"❓ No match → 'unknown'")

    print(f"📤 FINAL: {result} | score: {max_score:.4f}")
    print(f"{'='*60}\n")

    return result, max_score


