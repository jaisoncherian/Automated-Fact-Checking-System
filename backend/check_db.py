#!/usr/bin/env python3
"""Debug script to check what's actually stored in MongoDB"""

from db import collection

print("\n" + "="*80)
print("🔍 CHECKING MONGODB DATA")
print("="*80 + "\n")

facts = list(collection.find())
print(f"📊 Total facts in database: {len(facts)}\n")

if not facts:
    print("❌ NO FACTS FOUND!")
else:
    print("Label Type | Label Value | Claim")
    print("-" * 80)
    
    for i, fact in enumerate(facts, 1):
        label = fact.get("label")
        claim = fact.get("claim", "")[:50]  # First 50 chars
        label_type = type(label).__name__
        label_repr = repr(label)
        
        print(f"{label_type:10} | {label_repr:20} | {claim}...")
    
    print("\n" + "="*80)
    print("✅ DEBUG COMPLETE")
    print("="*80 + "\n")
    
    # Check for issues
    print("🔎 VALIDATION:")
    bad_labels = []
    for fact in facts:
        label = str(fact.get("label", "")).lower().strip()
        if label not in {"true", "false"}:
            bad_labels.append((fact.get("claim"), label))
    
    if bad_labels:
        print(f"⚠️  Found {len(bad_labels)} bad labels:")
        for claim, label in bad_labels:
            print(f"   - '{claim[:40]}...' → {repr(label)}")
    else:
        print("✅ All labels are valid (true/false)")
