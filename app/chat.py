from app.extractor import extract_constraints
from app.retriever import BM25Retriever

retriever = BM25Retriever("data/catalog.json")


def chat(messages):
    conversation = "\n".join(
        f"{m.role}: {m.content}"
        for m in messages
    )

    conversation_lower = conversation.lower()

    # -----------------------------
    # Turn limit
    # -----------------------------
    user_turns = sum(1 for m in messages if m.role.lower() == "user")

    if user_turns >= 8:
        return {
            "reply": "We've reached the conversation limit. Please start a new conversation for additional assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": True
        }

    # -----------------------------
    # Prompt injection protection
    # -----------------------------
    injection_keywords = [
        "ignore previous instructions",
        "ignore all instructions",
        "reveal system prompt",
        "show system prompt",
        "act as",
        "pretend to be",
        "developer mode",
        "jailbreak"
    ]

    if any(keyword in conversation_lower for keyword in injection_keywords):
        return {
            "reply": "I'm designed only to help with SHL assessment recommendations and cannot follow requests that change my instructions.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Off-topic detection
    # -----------------------------
    off_topic = [
        "weather",
        "football",
        "cricket",
        "movie",
        "recipe",
        "politics",
        "bitcoin",
        "stock market"
    ]

    if any(word in conversation_lower for word in off_topic):
        return {
            "reply": "I'm designed to help only with SHL assessment recommendations.",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Extract constraints
    # -----------------------------
    constraints = extract_constraints(conversation)

    role = constraints.get("role", "").strip()
    seniority = constraints.get("seniority", "").strip()
    skills = constraints.get("skills", [])

    # -----------------------------
    # Clarification
    # -----------------------------
    if not role:
        return {
            "reply": "What job role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    if not seniority:
        return {
            "reply": "What is the seniority level (Junior, Mid, Senior, Lead)?",
            "recommendations": [],
            "end_of_conversation": False
        }

    # -----------------------------
    # Search
    # -----------------------------
    query = " ".join([role, seniority] + skills)

    results = retriever.search(query, top_k=10)

    # -----------------------------
    # Compare support
    # -----------------------------
    if "compare" in conversation_lower and len(results) >= 2:

        a = results[0]
        b = results[1]

        return {
            "reply": (
                f"Comparison:\n\n"
                f"{a['title']}: {a['description']}\n\n"
                f"{b['title']}: {b['description']}"
            ),
            "recommendations": [
                {
                    "name": a["title"],
                    "url": a["url"],
                    "test_type": "Assessment"
                },
                {
                    "name": b["title"],
                    "url": b["url"],
                    "test_type": "Assessment"
                }
            ],
            "end_of_conversation": False
        }

    # -----------------------------
    # Build recommendations
    # -----------------------------
    recommendations = []

    for item in results:

        title = item["title"].lower()
        description = item["description"].lower()

        text = f"{title} {description}"

        if "personality" in text or "opq" in text or "motivational" in text:
            test_type = "Personality"

        elif "technical" in text or "coding" in text:
            test_type = "Technical"

        elif "cognitive" in text or "reasoning" in text or "verify" in text:
            test_type = "Cognitive"

        elif "behavior" in text or "situational" in text or "competency" in text:
            test_type = "Behavioral"

        elif "simulation" in text:
            test_type = "Simulation"

        elif "development" in text:
            test_type = "Development"

        else:
            test_type = "Assessment"

        recommendations.append({
            "name": item["title"],
            "url": item["url"],
            "test_type": test_type
        })

    return {
        "reply": f"I found {len(recommendations)} SHL assessments matching your requirements.",
        "recommendations": recommendations,
        "end_of_conversation": False
    }