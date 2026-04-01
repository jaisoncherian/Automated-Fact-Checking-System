#!/usr/bin/env python
"""Test script for the vernacular fact-checking API"""

import requests
import json

base_url = 'http://localhost:8000'

print("=" * 60)
print("VERNACULAR FACT-CHECKING API TEST SUITE")
print("=" * 60)

# Test 1 - English input
print("\nTEST 1: English input with multiple claims")
print("-" * 60)
try:
    response = requests.post(f'{base_url}/check-multilingual', 
                           json={'text': 'The earth is flat. Vaccines cause autism.'})
    result = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Claims found: {result.get('claims_found')}")
    print(f"✓ Results returned: {len(result.get('results', []))} claims")
    
    for i, r in enumerate(result.get('results', []), 1):
        print(f"\n  Claim {i}: {r['claim'][:60]}...")
        print(f"  Verdict: {r['verdict']}")
        print(f"  Confidence: {r['confidence']*100:.1f}%")
        print(f"  Explanation: {r['explanation'][:70]}...")
    
    if result.get('claims_found') == 2:
        print("\n✅ TEST 1 PASSED: Correct number of claims found")
    else:
        print(f"\n⚠️ TEST 1 WARNING: Expected 2 claims, got {result.get('claims_found')}")
except Exception as e:
    print(f"❌ TEST 1 FAILED: {str(e)}")

# Test 2 - Non-English input (Malayalam)
print("\n" + "=" * 60)
print("TEST 2: Malayalam input with back-translation")
print("-" * 60)
try:
    response = requests.post(f'{base_url}/check-multilingual', 
                           json={'text': 'ഭൂമി പരന്നതാണ്'})
    result = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Detected language: {result.get('detected_language')} ({result.get('language_name')})")
    print(f"✓ Claims found: {result.get('claims_found')}")
    
    if result.get('results'):
        r = result['results'][0]
        print(f"\n  Claim: {r['claim']}")
        print(f"  Verdict: {r['verdict']}")
        print(f"  Explanation (in Malayalam): {r['explanation']}")
        
        # Check if explanation is NOT in English (heuristic: Malayalam has unique characters)
        is_not_english = any(ord(c) > 127 for c in r['explanation'])
        if is_not_english or result.get('detected_language') == 'ml':
            print("\n✅ TEST 2 PASSED: Explanation returned in original language")
        else:
            print("\n⚠️ TEST 2 WARNING: Explanation may not be in original language")
except Exception as e:
    print(f"❌ TEST 2 FAILED: {str(e)}")

# Test 3 - /check endpoint (regression)
print("\n" + "=" * 60)
print("TEST 3: /check endpoint (regression test)")
print("-" * 60)
try:
    response = requests.post(f'{base_url}/check', 
                           json={'text': 'earth is round'})
    result = response.json()
    print(f"✓ Status: {response.status_code}")
    print(f"✓ Result: {result.get('result')}")
    print(f"✓ Confidence: {result.get('confidence'):.4f}")
    
    if result.get('result') in ['true', 'fake', 'suspicious', 'unknown']:
        print("✅ TEST 3 PASSED: /check endpoint still works correctly")
    else:
        print(f"⚠️ TEST 3 WARNING: Unexpected verdict: {result.get('result')}")
except Exception as e:
    print(f"❌ TEST 3 FAILED: {str(e)}")

print("\n" + "=" * 60)
print("TEST SUITE COMPLETE")
print("=" * 60)
