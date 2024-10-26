from rest_framework import serializers
from .models import LogEntry

class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry
        fields = ['timestamp', 'service_name', 'log_content', 'log_hash', 'is_verified']

class LogQuerySerializer(serializers.Serializer):
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    service_name = serializers.CharField(required=False)

class LogIngestionSerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    service_name = serializers.CharField()
    log_content = serializers.CharField()