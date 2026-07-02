import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")


def recommend_assessments(user_query, candidates):
    prompt = f"""
You are an SHL assessment recommendation assistant.

User conversation:

{user_query}

Candidate assessments:

{json.dumps(candidates, indent=2)}

Choose the best matching assessments.

Return ONLY valid JSON.

Example:

{{
  "recommended_assessments": [
    {{
      "name": "Technical Skills",
      "url": "https://www.shl.com/...",
      "test_type": "Technical"
    }}
  ]
}}

Rules:
- Recommend between 1 and 10 assessments.
- Use ONLY the candidate assessments provided.
- Never invent assessment names or URLs.
- test_type must be one of:
  Technical, Personality, Behavioral, Cognitive, Simulation, Development.
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    return json.loads(text)