import json

from django.contrib.auth.models import User
from rest_framework import serializers

from .models import DomainEvent


class DomainEventWriteSerializer(serializers.ModelSerializer):
    payload = serializers.JSONField(source='blob')
    created = serializers.DateTimeField(source='date_occurred')
    created_by = serializers.CharField(source='username')

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'payload',
            'created',
            'created_by',
        )
    
    def create(self, validated_data):
        validated_data['blob'] = json.dumps(validated_data['blob'], indent=2)
        return DomainEvent.objects.create(**validated_data)
    
    def validate_created_by(self, value):
        if not User.objects.filter(username=value).exists():
            raise User.DoesNotExist("Cannot find username matching '{}'".format(value))
        return value

class DomainEventReadSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='username')

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
    
    def get_created(self, obj):
        return obj.date_occurred

    def get_payload(self, obj):
        return json.loads(obj.blob)
