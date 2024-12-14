import os
import json
from django.core.management.base import BaseCommand
from core.models import Sort


class Command(BaseCommand):
    help = "Charge les données des sorts depuis des fichiers JSON."

    def handle(self, *args, **kwargs):
        folder_path = "scrapers/codex_scraper/output"

        if not os.path.exists(folder_path):
            self.stderr.write(self.style.ERROR(f"Le dossier {folder_path} n'existe pas."))
            return

        files_loaded = 0

        for file_name in os.listdir(folder_path):
            if file_name.startswith("sorts_") and file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        Sort.objects.create(
                            title=data["title"],
                            description=data.get("description", ""),
                            prerequisites=data.get("prerequisites", ""),
                            source=data.get("source", ""),
                            url=data.get("url", ""),
                        )

                        files_loaded += 1
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"Erreur lors du chargement de {file_name} : {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"{files_loaded} fichiers de sorts chargés avec succès.")
        )
