import json
import os


class JsonPerUrlPipeline:
    def process_item(self, item, spider):
        # Générer un nom de fichier unique basé sur l'URL
        url = item.get("title", "default")
        filename = url.replace(" ", "_").replace("/", "_").replace("?", "_") + ".json"

        # Créer le dossier de sortie s'il n'existe pas
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)
        file_path = os.path.join(output_dir, filename)

        # Sauvegarder l'item dans un fichier JSON
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(item, f, ensure_ascii=False, indent=4)

        spider.logger.info(f"Saved data to {file_path}")
        return item
