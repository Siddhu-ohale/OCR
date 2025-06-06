
import requests
import json
from dotenv import load_dotenv
import re
import logging
import os 

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"

def ask_gemini_to_parse(raw_text: str) -> dict:
    prompt = f"""
Extract structured data in JSON format from the following OCR text:

```{raw_text}```

Required fields (if available):
- ID number (Aadhaar / PAN / Voter ID)
- name
- date_of_birth
- gender
- father's name
- document type

Return valid JSON inside triple backticks.
"""
    payload = {
        "contents": [{
            "parts": [{"text": prompt.strip()}]
        }]
    }

    response = requests.post(GEMINI_URL, headers={"Content-Type": "application/json"}, json=payload)

    if response.status_code == 200:
        gemini_text = response.json()["candidates"][0]["content"]["parts"][0]["text"]
        match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", gemini_text, re.DOTALL)
        if match:
            json_string = match.group(1)
            try:
                return json.loads(json_string)
            except json.JSONDecodeError:
                return {"error": "Invalid JSON", "raw_response": gemini_text}
        else:
            return {"error": "No JSON block found", "raw_response": gemini_text}

    return {"error": "Gemini API request failed", "status": response.status_code, "message": response.text}
