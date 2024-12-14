import os
import json
import pandas as pd

# Chemin vers le dossier contenant les fichiers JSON
folder_path = "scrapers\codex_scraper\output"

# Initialiser le rapport d'analyse
analysis = {}

# Parcourir les fichiers dans le dossier
for file_name in os.listdir(folder_path):
    if not file_name.endswith(".json"):
        continue

    category = file_name.split("_")[0]  # Extraire la catégorie
    if category not in analysis:
        analysis[category] = {"files": 0, "fields": {}, "errors": 0}

    file_path = os.path.join(folder_path, file_name)
    try:
        # Charger le fichier JSON
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Mettre à jour le nombre de fichiers
        analysis[category]["files"] += 1

        # Mettre à jour les champs
        for key in data.keys():
            if key not in analysis[category]["fields"]:
                analysis[category]["fields"][key] = 0
            analysis[category]["fields"][key] += 1
    except Exception as e:
        analysis[category]["errors"] += 1
        print(f"Erreur avec {file_name}: {e}")

# Générer un rapport sous forme de DataFrame
report_data = []
for category, stats in analysis.items():
    for field, count in stats["fields"].items():
        report_data.append({
            "Category": category,
            "Field": field,
            "Occurrence": count,
            "Total Files": stats["files"],
            "Errors": stats["errors"]
        })

df_report = pd.DataFrame(report_data)

# Sauvegarder le rapport
output_report = "scrapers/codex_scraper/analysis_report.csv"
df_report.to_csv(output_report, index=False)

print(f"Analyse terminée. Rapport sauvegardé dans {output_report}.")
