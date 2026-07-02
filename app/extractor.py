import os
import json
from dotenv import load_dotenv
import google.generativeai as genai
from pydantic import BaseModel, ValidationError

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")


# -----------------------------
# Pydantic Model
# -----------------------------
class Constraints(BaseModel):
    role: str
    seniority: str
    skills: list[str]
    keywords: str


# -----------------------------
# Constraint Extraction Function
# -----------------------------
def extract_constraints(query):
    prompt = f"""
You are an AI assistant for SHL assessment recommendations.

Extract the hiring requirements from the user's query.

Return ONLY a valid JSON object.

Rules:
- Do NOT use markdown.
- Do NOT use code fences.
- Do NOT include explanations.
- Always include all four fields.
- If information is missing, leave it as an empty string or empty list.

Format:

{{
    "role": "",
    "seniority": "",
    "skills": [],
    "keywords": ""
}}

Extract:
- Job role
- Seniority level (Junior, Mid, Senior, Lead, etc.)
- ALL technical and soft skills
- keywords should be a single search string combining the important information.

User Query:
{query}
"""

    # Retry once if Gemini returns invalid output
    for attempt in range(2):

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
            data = json.loads(text)

            validated = Constraints.model_validate(data)

            return validated.model_dump()

        except (json.JSONDecodeError, ValidationError) as e:

            print(f"Attempt {attempt + 1} failed.")
            print(text)
            print(e)

            # Retry once
            if attempt == 0:
                continue

    # Safe fallback
    return {
        "role": "",
        "seniority": "",
        "skills": [],
        "keywords": query
    }