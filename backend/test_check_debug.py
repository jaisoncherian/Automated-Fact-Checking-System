#!/usr/bin/env python
"""Debug: Check server response"""

import requests

base_url = 'http://localhost:5000'

try:
    response = requests.post(f'{base_url}/check', 
        json={'text': 'ഭൂമി പരന്നതാണ്'})
    print(f'Status Code: {response.status_code}')
    print(f'Headers: {dict(response.headers)}')
    print(f'Text: {response.text[:200]}')
except Exception as e:
    print(f'Error: {e}')
