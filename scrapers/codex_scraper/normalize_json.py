import os
import json
import pandas as pd

# Chemin vers le dossier contenant les fichiers JSON
input_folder = "scrapers\\codex_scraper\\output"
output_file = "scrapers\\codex_scraper\\normalized_data.csv"

# Définir le schéma cible
global_schema = {
    "actions": None,
    "class_abilities": None,
    "description": None,
    "etats": None,
    "exhaustion": None,
    "image_url": None,
    "images": None,
    "internal_links": None,
    "introduction": None,
    "links": None,
    "prerequisites": None,
    "reactions": None,
    "sections": None,
    "skills": None,
    "source": None,
    "special_boxes": None,
    "stats": None,
    "table": None,
    "tables": None,
    "title": None,
    "titre": None,
    "traduction": None,
    "type_rarete": None,
    "url": None,
}


# Fonction de normalisation
def normalize_data(data, schema):
    normalized = {key: data.get(key, schema[key]) for key in schema}
    return normalized


# Fusionner les fichiers JSON
all_data = []
errors = []

for file_name in os.listdir(input_folder):
    if file_name.endswith(".json"):
        file_path = os.path.join(input_folder, file_name)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                normalized = normalize_data(data, global_schema)
                all_data.append(normalized)
        except Exception as e:
            errors.append(f"{file_name}: {e}")

# Créer un DataFrame Pandas
df = pd.DataFrame(all_data)

# Sauvegarder en CSV
df.to_csv(output_file, index=False)

# Log des erreurs
with open("error_log.txt", "w") as log_file:
    log_file.write("\n".join(errors))

print(f"Normalisation terminée. Données sauvegardées dans {output_file}.")
