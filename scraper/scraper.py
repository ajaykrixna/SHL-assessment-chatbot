import json
import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/138.0 Safari/537.36"
    )
}

category_urls = [
    "https://www.shl.com/products/assessments/behavioral-assessments/",
    "https://www.shl.com/products/assessments/personality-assessment/",
    "https://www.shl.com/products/assessments/cognitive-assessments/",
    "https://www.shl.com/products/assessments/skills-and-simulations/",
    "https://www.shl.com/products/assessments/job-focused-assessments/"
]

all_assessments = []

for url in category_urls:
    print(f"Scraping: {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Failed: {response.status_code}")
        continue

    soup = BeautifulSoup(response.text, "html.parser")

    cards = soup.select("div.content-card")

    print(f"Found {len(cards)} cards")

    for card in cards:
        title_tag = card.find("h3", class_="content-card__title")
        desc_tag = card.find("div", class_="content-card__content")
        link_tag = card.find("a", href=True)

        if not title_tag or not link_tag:
            continue

        title = title_tag.get_text(strip=True)
        description = (
            desc_tag.get_text(" ", strip=True)
            if desc_tag else ""
        )

        link = link_tag["href"]

        if link.startswith("/"):
            link = "https://www.shl.com" + link

        all_assessments.append({
            "title": title,
            "description": description,
            "url": link
        })

# Remove duplicates
unique = []
seen = set()

for assessment in all_assessments:
    if assessment["url"] not in seen:
        unique.append(assessment)
        seen.add(assessment["url"])

with open("data/catalog.json", "w", encoding="utf-8") as f:
    json.dump(unique, f, indent=4, ensure_ascii=False)

print(f"\nSaved {len(unique)} assessments to data/catalog.json")