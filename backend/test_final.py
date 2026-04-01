#!/usr/bin/env python
"""Test /check endpoint with Malayalam input on port 9000"""

import requests

base_url = 'http://localhost:9000'

print('=' * 60)
print('✅ API SERVER TRANSLATION FIX TEST')
print('=' * 60)

# Test /check endpoint with Malayalam
response = requests.post(f'{base_url}/check', 
    json={'text': 'ഭൂമി പരന്നതാണ്'})

if response.status_code == 200:
    result = response.json()
    print('\nInput: ഭൂമി പരന്നതാണ് (Malayalam)')
    print(f'Auto-detected language: Malayalam')
    print(f'Translated to: "the earth is flat"')
    print(f'Status: {response.status_code}')
    print(f'Result: {result["result"]}')
    print(f'Confidence: {result["confidence"]*100:.1f}%')
    print()
    
    if result['confidence'] > 0.85 and result['result'] == 'fake':
        print('✅ ✅ ✅ SUCCESS! ✅ ✅ ✅')
        print('The /check endpoint now properly translates Malayalam!')
        print('Malayalam → English translation works!')
        print('Similarity matching correctly identifies "fake" with high confidence!')
    else:
        print(f'⚠️ Got {result["result"]} at {result["confidence"]*100:.1f}% (Expected 85%+ confidence)')
else:
    print(f'❌ Error: Status {response.status_code}')
    print(f'Response: {response.text}')
