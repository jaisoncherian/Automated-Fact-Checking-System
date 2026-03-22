#!/usr/bin/env python3
"""Quick test to verify verdict cleaning is working"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from similarity import check_fact

# Test claims
test_claims = [
    "The Earth is round",
    "Earth orbits the Sun",
    "Water boils at 100 degrees Celsius",
    "The moon is made of cheese",
    "Gravity pulls objects downward"
]

print("\n" + "="*70)
print("🧪 TESTING VERDICT CLEANING FIX")
print("="*70)

for claim in test_claims:
    print(f"\n📝 Testing: {claim}")
    verdict, score = check_fact(claim)
    
    # Check for hidden characters
    verdict_codes = [ord(c) for c in verdict]
    print(f"✅ Verdict: '{verdict}'")
    print(f"   Character codes: {verdict_codes}")
    print(f"   Confidence: {score:.4f}")
    
    # Validate verdict is clean
    valid = {"true", "false", "suspicious", "unknown"}
    if verdict in valid:
        print(f"   ✓ VALID verdict (no hidden chars)")
    else:
        print(f"   ✗ INVALID verdict! (unexpected characters)")

print("\n" + "="*70)
print("✅ Test complete!")
print("="*70 + "\n")
