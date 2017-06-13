import json

from rest_framework import serializers

from .models import DomainEvent


class DomainEventReadSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    created_by = serializers.SerializerMethodField()

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'created_by',
            'created',
            'payload',
        )

    def get_created_by(self, obj):
        return obj.username
    
    def get_created(self, obj):
        return obj.date_occurred

    def get_payload(self, obj):
        return json.loads(obj.blob)
