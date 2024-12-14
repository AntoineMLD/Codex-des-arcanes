import os
import json
from django.core.management.base import BaseCommand
from core.models import Classe, Section, Table


class Command(BaseCommand):
    help = "Recharge les données des classes depuis des fichiers JSON."

    def handle(self, *args, **kwargs):
        folder_path = "scrapers/codex_scraper/output"

        if not os.path.exists(folder_path):
            self.stderr.write(self.style.ERROR(f"Le dossier {folder_path} n'existe pas."))
            return

        files_loaded = 0

        for file_name in os.listdir(folder_path):
            if file_name.startswith("classes_") and file_name.endswith(".json"):
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)

                        # Insérer les données de la classe
                        classe = Classe.objects.create(
                            title=data["title"], introduction=data.get("introduction", "")
                        )

                        # Insérer les sections associées
                        for section in data.get("sections", []):
                            Section.objects.create(
                                classe=classe,
                                title=section.get("title", ""),
                                content=section.get("content", ""),
                            )

                        # Insérer les tables associées
                        tables = data.get("tables", {})
                        if isinstance(tables, dict):  # Si tables est un dictionnaire
                            for table_name, table_data in tables.items():
                                if isinstance(table_data, list) and table_data:
                                    headers = list(
                                        table_data[0].keys()
                                    )  # Utiliser les clés comme headers
                                    structured_data = {"headers": headers, "rows": table_data}
                                    Table.objects.create(
                                        classe=classe, title=table_name, data=structured_data
                                    )
                        elif isinstance(tables, list):  # Si tables est une liste
                            for table in tables:
                                Table.objects.create(
                                    classe=classe,
                                    title=table.get("name", ""),
                                    data=table.get("data", []),
                                )

                        files_loaded += 1
                except Exception as e:
                    self.stderr.write(
                        self.style.ERROR(f"Erreur lors du chargement de {file_name} : {e}")
                    )

        self.stdout.write(
            self.style.SUCCESS(f"{files_loaded} fichiers de classes chargés avec succès.")
        )
