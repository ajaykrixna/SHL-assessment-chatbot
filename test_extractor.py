from app.extractor import extract_constraints

query = "I need a senior Java developer with leadership skills."

result = extract_constraints(query)

print(result)