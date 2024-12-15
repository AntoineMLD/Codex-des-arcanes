import os
import json
import requests

# Dossier contenant les fichiers JSON principaux
INPUT_FOLDER = "api_output"
# Dossier de sortie pour les données extraites
OUTPUT_FOLDER = "api_detailed_output"

# URL de base de l'API
BASE_URL = "https://www.dnd5eapi.co"

# Liste complète des routes à parcourir
ROUTES = [
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

# Créer le dossier de sortie s'il n'existe pas
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# Fonction pour lire un fichier JSON
def read_json(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)


# Fonction pour sauvegarder un fichier JSON
def save_json(data, filepath):
    if os.path.exists(filepath):
        print(f"Le fichier existe déjà, il ne sera pas écrasé : {filepath}")
        return  # Ne pas écraser le fichier
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Fonction pour récupérer les données d'une URL
def fetch_data(url):
    full_url = f"{BASE_URL}{url}" if not url.startswith(BASE_URL) else url
    print(f"Requête envoyée à : {full_url}")
    response = requests.get(full_url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Erreur {response.status_code} pour {full_url}")
        return None


# Fonction pour traiter les classes
def process_class(class_data, class_name):
    class_folder = os.path.join(OUTPUT_FOLDER, class_name)
    os.makedirs(class_folder, exist_ok=True)

    # Vérifier la présence de "spells"
    spells_url = class_data.get("spells")
    if isinstance(spells_url, str) and spells_url.startswith("/api/"):
        spells_folder = os.path.join(class_folder, "spells")
        os.makedirs(spells_folder, exist_ok=True)
        spells_filepath = os.path.join(spells_folder, "spells.json")
        if not os.path.exists(spells_filepath):
            spells_data = fetch_data(f"{BASE_URL}{spells_url}")
            if spells_data:
                save_json(spells_data, spells_filepath)
    elif isinstance(spells_url, list):
        spells_folder = os.path.join(class_folder, "spells")
        os.makedirs(spells_folder, exist_ok=True)
        for spell_entry in spells_url:
            spell_data = spell_entry.get("spell", {})
            spell_url = spell_data.get("url")
            spell_name = spell_data.get("index")
            if spell_url and spell_url.startswith("/api/"):
                spell_filepath = os.path.join(spells_folder, f"{spell_name}.json")
                if not os.path.exists(spell_filepath):
                    spell_data = fetch_data(f"{BASE_URL}{spell_url}")
                    if spell_data:
                        save_json(spell_data, spell_filepath)

    # Vérifier la présence de "subclasses"
    subclasses = class_data.get("subclasses", [])
    if subclasses:
        subclasses_folder = os.path.join(class_folder, "subclasses")
        os.makedirs(subclasses_folder, exist_ok=True)
        for subclass in subclasses:
            subclass_name = subclass.get("index")
            subclass_url = subclass.get("url")
            if subclass_url and subclass_url.startswith("/api/"):
                subclass_filepath = os.path.join(subclasses_folder, f"{subclass_name}.json")
                if not os.path.exists(subclass_filepath):
                    subclass_data = fetch_data(f"{BASE_URL}{subclass_url}")
                    if subclass_data:
                        save_json(subclass_data, subclass_filepath)


# Parcourir toutes les routes définies
for route in ROUTES:
    print(f"Récupération des données pour la route : {route}")
    route_folder = os.path.join(OUTPUT_FOLDER, route)
    os.makedirs(route_folder, exist_ok=True)

    # Récupérer les données principales pour chaque route
    route_data = fetch_data(f"/api/{route}")
    if route_data:
        save_json(route_data, os.path.join(route_folder, f"{route}.json"))

        # Traiter les éléments individuels dans les routes complexes
        if route == "classes":
            for class_entry in route_data.get("results", []):
                class_url = class_entry.get("url")
                class_name = class_entry.get("index")
                if class_url:
                    detailed_class_data = fetch_data(class_url)
                    if detailed_class_data:
                        process_class(detailed_class_data, class_name)
        else:
            for item in route_data.get("results", []):
                item_name = item.get("index")
                item_url = item.get("url")
                if item_url and item_url.startswith("/api/"):
                    item_filepath = os.path.join(route_folder, f"{item_name}.json")
                    if not os.path.exists(item_filepath):
                        detailed_item_data = fetch_data(item_url)
                        if detailed_item_data:
                            save_json(detailed_item_data, item_filepath)
