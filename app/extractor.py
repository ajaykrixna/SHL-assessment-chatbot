import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


def extract_constraints(query):
    prompt = f"""
You are an AI assistant for SHL assessment recommendations.

Extract the hiring requirements from the user's query.

Return ONLY valid JSON.

Format:
{{
    "role": "",
    "seniority": "",
    "skills": [],
    "keywords": ""
}}

Rules:
- Extract the job role.
- Extract the seniority level (Junior, Mid, Senior, Lead, etc.).
- Extract ALL technical and soft skills.
- keywords should be a single search string combining the important information.
- Do not include explanations.
- Return JSON only.

User Query:
{query}
"""

    response = model.generate_content(prompt)

    text = response.text.strip()

    # Remove markdown if Gemini returns ```json
    if text.startswith("```json"):
        text = text.replace("```json", "", 1)

    if text.startswith("```"):
        text = text.replace("```", "", 1)

    if text.endswith("```"):
        text = text[:-3]

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        print("Failed to parse Gemini response:")
        print(text)
        raise