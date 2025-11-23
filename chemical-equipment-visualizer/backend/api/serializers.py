from rest_framework import serializers
from .models import Dataset

class DatasetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["id", "created_at", "original_filename", "summary_json", "columns", "preview_rows"]

class UploadResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    message = serializers.CharField()
    summary = serializers.JSONField()
    columns = serializers.ListField(child=serializers.CharField())
    preview_rows = serializers.ListField()
