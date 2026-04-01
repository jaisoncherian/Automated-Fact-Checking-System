# Quick Reference: Vernacular Fact-Checking API

## Quick Start

### 1. Start the API Server
```bash
cd backend
python -m uvicorn api:app --reload
```
Server runs on: `http://localhost:8000`

### 2. Test MultilIngual Endpoint

#### Using curl (English example):
```bash
curl -X POST http://localhost:8000/check-multilingual \
  -H "Content-Type: application/json" \
  -d '{"text":"The Earth is flat"}'
```

#### Using Python requests:
```python
import requests

response = requests.post(
    "http://localhost:8000/check-multilingual",
    json={"text": "The Earth is round"}
)
print(response.json())
```

#### Using fetch (JavaScript):
```javascript
fetch('http://localhost:8000/check-multilingual', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({text: "The Earth is round"})
})
.then(r => r.json())
.then(data => console.log(data))
```

---

## API Response Format

### Success Response (200)
```json
{
  "original_text": "The Earth is round",
  "english_translation": "The Earth is round",
  "detected_language": "en",
  "language_name": "English",
  "verdict": "true",
  "verdict_explanation": "This statement is TRUE",
  "verdict_in_original_language": "This statement is TRUE",
  "confidence": 1.0
}
```

### Error Response (400/500)
```json
{
  "detail": "Text cannot be empty"
}
```

---

## Supported Verdicts

| Verdict | Meaning |
|---------|---------|
| `true` | Claim is verified as TRUE |
| `fake` | Claim is verified as FALSE |
| `suspicious` | Claim cannot be verified or is uncertain |
| `unknown` | No matching fact found in database |

---

## Language Codes Quick Reference

**South Indian Languages:**
- `ml` - Malayalam
- `ta` - Tamil
- `te` - Telugu
- `kn` - Kannada

**North Indian Languages:**
- `hi` - Hindi
- `gu` - Gujarati
- `ma` - Marathi
- `bn` - Bengali
- `pa` - Punjabi
- `ur` - Urdu

**International Languages:**
- `en` - English
- `fr` - French
- `de` - German
- `es` - Spanish
- `pt` - Portuguese
- `ja` - Japanese
- `ko` - Korean
- `zh-cn` - Chinese (Simplified)
- `ar` - Arabic

[Complete list via GET /supported-languages]

---

## Test Cases

### Test 1: Simple Fact Check
```bash
curl -X POST http://localhost:8000/check-multilingual \
  -H "Content-Type: application/json" \
  -d '{"text":"Water boils at 100 degrees"}'
# Expected: verdict = "true"
```

### Test 2: False Claim
```bash
curl -X POST http://localhost:8000/check-multilingual \
  -H "Content-Type: application/json" \
  -d '{"text":"The moon is made of cheese"}'
# Expected: verdict = "fake"
```

### Test 3: Unknown Claim
```bash
curl -X POST http://localhost:8000/check-multilingual \
  -H "Content-Type: application/json" \
  -d '{"text":"The sky is purple"}'
# Expected: verdict = "suspicious" or "unknown"
```

### Test 4: Specify Language
```bash
curl -X POST http://localhost:8000/check-multilingual \
  -H "Content-Type: application/json" \
  -d '{"text":"The Earth is round", "language":"en"}'
# Language field is optional - auto-detected if missing
```

---

## Batch Testing (Python)

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# List of test claims
test_claims = [
    "The Earth is round",
    "The Earth is flat",
    "Vaccines cause autism",
    "Vaccines are safe",
    "Fish need water to survive",
    "Humans can breathe underwater"
]

print("Testing Vernacular Fact-Checking API\n")
print("-" * 80)

for claim in test_claims:
    response = requests.post(
        f"{BASE_URL}/check-multilingual",
        json={"text": claim}
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nClaim: {claim}")
        print(f"Verdict: {data['verdict'].upper()}")
        print(f"Confidence: {data['confidence']:.2%}")
    else:
        print(f"Error: {response.status_code}")
```

---

## Debugging

### Check API Status
```bash
curl http://localhost:8000/
```
Should return:
```json
{
  "message": "Automated Vernacular Fact-Checking API",
  "version": "2.0",
  "endpoints": {...}
}
```

### Get Supported Languages
```bash
curl http://localhost:8000/supported-languages | python -m json.tool
```

### Run Test Suite
```bash
cd backend
python test_vernacular.py
```

### View API Docs
```
http://localhost:8000/docs       # Swagger UI
http://localhost:8000/redoc      # ReDoc
```

---

## Common Issues & Solutions

**Issue**: "Connection refused"
- **Solution**: Make sure API is running with `uvicorn api:app --reload`

**Issue**: "Text cannot be empty" 
- **Solution**: Ensure JSON body includes non-empty `text` field

**Issue**: Translation taking too long
- **Solution**: Translation API has rate limits. Wait a few seconds and retry

**Issue**: Always getting "suspicious" verdict
- **Solution**: Claim not in database. Add more facts to MongoDB

**Issue**: Language not detected correctly
- **Solution**: Text must be 10+ characters and primarily one language

**Issue**: ModuleNotFoundError
- **Solution**: Install requirements: `pip install -r requirements.txt`

---

## Performance Tips

1. **Batch multiple claims**: Don't make API call per character
2. **Cache translations**: Store translated versions locally
3. **Use mock data**: Falls back automatically if MongoDB unavailable
4. **Connection pooling**: FastAPI handles this automatically
5. **Async requests**: API supports concurrent requests

---

## Example Frontend Integration

### React Component
```javascript
import React, { useState } from 'react';

function VernacularFactChecker() {
  const [text, setText] = useState('');
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const checkFact = async () => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:8000/check-multilingual', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      const data = await response.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <input value={text} onChange={e => setText(e.target.value)} />
      <button onClick={checkFact} disabled={loading}>
        {loading ? 'Checking...' : 'Check Fact'}
      </button>
      
      {result && (
        <div>
          <h3>Verdict: {result.verdict.toUpperCase()}</h3>
          <p>Language: {result.language_name}</p>
          <p>Confidence: {(result.confidence * 100).toFixed(1)}%</p>
          <p>Result: {result.verdict_in_original_language}</p>
        </div>
      )}
    </div>
  );
}
```

---

## Version Info

- **API Version**: 2.0
- **Python**: 3.10+
- **FastAPI**: 0.135.1
- **Key Dependencies**:
  - langdetect (language detection)
  - sentence-transformers (semantic similarity)
  - pymongo (database)
  - googletrans (translation)

---

**Last Updated**: 2026-04-01
