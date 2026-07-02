from app.extractor import extract_constraints
from app.retriever import BM25Retriever

retriever = BM25Retriever("data/catalog.json")


def chat(messages):
    conversation = "\n".join(
        f"{m.role}: {m.content}"
        for m in messages
    )

    conversation_lower = conversation.lower()

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

    constraints = extract_constraints(conversation)

    role = constraints.get("role", "").strip()
    seniority = constraints.get("seniority", "").strip()
    skills = constraints.get("skills", [])

    # Clarify if missing
    if not role:
        return {
            "reply": "What job role are you hiring for?",
            "recommendations": [],
            "end_of_conversation": False
        }

    if not seniority:
        return {
            "reply": "What is the seniority level (Junior, Mid, Senior)?",
            "recommendations": [],
            "end_of_conversation": False
        }

    query = " ".join([role, seniority] + skills)

    results = retriever.search(query, top_k=10)

    recommendations = []

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
        "end_of_conversation": True
    }