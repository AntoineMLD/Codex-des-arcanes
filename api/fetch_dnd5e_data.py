import requests
import json
import os

# Url de l'api
BASE_URL = "https://www.dnd5eapi.co/api"


# récupérer les données d'une route spécifique
def fetch_data(route):
    url = f"{BASE_URL}/{route}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error {response.status_code} for {route}")
        return None


# Sauvegarder les données dans un fichier json
def save_to_json(data, filename):
    os.makedirs("api_output", exist_ok=True)
    with open(f"api_output/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# routes à parcourir
routes = [
    "ability-scores",
    "alignments",
    "backgrounds",
    "classes",
    "conditions",
    "damage-types",
    "equipment",
    "equipment-categories",
    "feats",
    "features",
    "languages",
    "magic-items",
    "magic-schools",
    "monsters",
    "proficiencies",
    "races",
    "rule-sections",
    "rules",
    "skills",
    "spells",
    "subclasses",
    "subraces",
    "traits",
    "weapon-properties",
]
routes = [
    "/api/classes/sorcerer/spells",
    "/api/subclasses/berserker",
    "/api/classes/bard/spells",
    "/api/classes/cleric/spells",
]

if __name__ == "__main__":
    for route in routes:
        print(f"save data for {route}...")
        data = fetch_data(route)
        if data:
            save_to_json(data, route)
            print(f"data for {route} saved successfully !")
