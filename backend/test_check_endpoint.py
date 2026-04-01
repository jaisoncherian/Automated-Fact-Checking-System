#!/usr/bin/env python
"""Test /check endpoint with Malayalam input"""

import requests
import json

base_url = 'http://localhost:5000'

print('=' * 60)
print('TEST: /check endpoint with Malayalam input')
print('=' * 60)

response = requests.post(f'{base_url}/check', 
    json={'text': 'ഭൂമി പരന്നതാണ്'})
result = response.json()

print('Input: ഭൂമി പരന്നതാണ് (Malayalam: "The earth is flat")')
print(f'Status: {response.status_code}')
print(f'Result: {result["result"]}')
print(f'Confidence: {result["confidence"]*100:.1f}%')

if result['confidence'] > 0.85 and result['result'] == 'fake':
    print()
    print('✅ SUCCESS! Translation fix works!')
    print('   - Malayalam translated correctly')
    print('   - Matched DB entry with high confidence')
    print('   - Returned FAKE verdict')
else:
    print()
    print(f'❌ Issue: Got {result["result"]} at {result["confidence"]*100:.1f}% (Expected fake at 85%+)')
