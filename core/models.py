from django.db import models

class StagingData(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    source_url = models.URLField()
    scraped_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
