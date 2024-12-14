import os
import json

# Chemin vers le dossier contenant les fichiers JSON
folder_path = "scrapers\\codex_scraper\\output"


# Fonction pour extraire le nom de fichier à partir de l'URL
def extract_filename(data):
    try:
        url = data.get("url", "")
        if "dnd/" in url and "=" in url:
            category = url.split("dnd/")[1].split(".")[0]  # Catégorie entre 'dnd/' et '.'
            name = url.split("=")[-1]  # Dernier mot après '='
            return f"{category}_{name}.json"
    except Exception as e:
        print(f"Erreur lors du traitement de l'URL : {e}")
    return None


# Renommer les fichiers
for file_name in os.listdir(folder_path):
    if not file_name.endswith(".json"):
        continue

    file_path = os.path.join(folder_path, file_name)
    try:
        # Charger le contenu JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extraire le nouveau nom de fichier
        new_name = extract_filename(data)
        if new_name:
            new_path = os.path.join(folder_path, new_name)
            os.rename(file_path, new_path)
            print(f"Renommé : {file_name} -> {new_name}")
        else:
            print(f"Aucun changement : {file_name}")
    except Exception as e:
        print(f"Erreur avec {file_name}: {e}")
