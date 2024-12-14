from django.db import models


# Modèle pour les Classes
class Classe(models.Model):
    title = models.CharField(max_length=255, unique=True)
    introduction = models.TextField()

    def __str__(self):
        return self.title


# Modèle pour les Sections
class Section(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="sections")
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


# Modèle pour les Tables
class Table(models.Model):
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE, related_name="tables")
    title = models.CharField(max_length=255)
    data = models.JSONField()

    def __str__(self):
        return self.title


class Don(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prerequisites = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title


class Origine(models.Model):
    title = models.CharField(max_length=255)
    introduction = models.TextField()
    sections = models.JSONField()
    tables = models.JSONField()

    def __str__(self):
        return self.title


class Regle(models.Model):
    title = models.CharField(max_length=255)
    introduction = models.TextField(null=True, blank=True)
    sections = models.JSONField()
    tables = models.JSONField(null=True, blank=True)
    url = models.URLField()

    def __str__(self):
        return self.title


class Sort(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    prerequisites = models.TextField(null=True, blank=True)
    source = models.CharField(max_length=255)
    url = models.URLField()

    def __str__(self):
        return self.title


class Monstre(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    stats = models.JSONField()  # Statistiques générales du monstre
    actions = models.JSONField()  # Actions que le monstre peut effectuer
    reactions = models.JSONField(
        null=True, blank=True
    )  # Réactions (doit être inclus pour corriger l'erreur)
    skills = models.JSONField(null=True, blank=True)  # Compétences du monstre
    url = models.URLField()  # URL de la page d'origine

    def __str__(self):
        return self.title
