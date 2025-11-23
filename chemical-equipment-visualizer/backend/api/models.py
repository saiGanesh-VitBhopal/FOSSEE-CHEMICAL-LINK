from django.db import models

class Dataset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    csv_file = models.FileField(upload_to="datasets/")
    original_filename = models.CharField(max_length=255)
    # Store computed values to speed up reads
    summary_json = models.JSONField()
    preview_rows = models.JSONField()  # first 20 rows (list of dicts)
    columns = models.JSONField()       # column names list

    def _str_(self):
        return f"{self.id} - {self.original_filename} ({self.created_at:%Y-%m-%d %H:%M})"