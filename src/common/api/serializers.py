import json

from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import DomainEvent, Project, Manufacturer

class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer

class ProjectSerializer(serializers.ModelSerializer):
    customer = serializers.SerializerMethodField()

    def get_customer(self, obj):
        return obj.manufacturer.name

    class Meta:
        model = Project
        fields = (
            'id',
            'code',
            'description',
            'date_created',
            'customer',
        )

class DomainEventWriteSerializer(serializers.ModelSerializer):
    payload = serializers.JSONField(source='blob')
    created = serializers.DateTimeField(source='date_occurred')
    created_by = serializers.CharField(source='owner.username')

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'object_id',
            'content_type',
            'event_type',
            'payload',
            'created',
            'created_by',
        )
    
    def create(self, validated_data):
        blob = json.dumps(validated_data.pop('blob'), indent=2)
        return DomainEvent.objects.create(blob=blob, **validated_data)
    
    def validate_created_by(self, value):
        if not User.objects.filter(username=value).exists():
            raise User.DoesNotExist("Cannot find username matching '{}'".format(value))
        return value

class DomainEventReadSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()
    created = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='owner.username')

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'object_id',
            'content_type',
            'event_type',
            'created_by',
            'created',
            'payload',
        )
    
    def get_created(self, obj):
        return obj.date_occurred

    def get_payload(self, obj):
        return json.loads(obj.blob)
