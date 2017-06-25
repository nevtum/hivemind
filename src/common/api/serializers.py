import json

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers

from ..models import DomainEvent, Manufacturer, Project


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField('get_user_full_name')

    def get_user_full_name(self, obj):
        return "{0} {1}".format(obj.first_name, obj.last_name)

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
    timestamp = serializers.DateTimeField(source='date_occurred')
    username = serializers.CharField()

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'payload',
            'timestamp',
            'username',
        )
    
    def create(self, validated_data):
        blob = json.dumps(validated_data.pop('blob'), indent=2)
        owner = User.objects.get(username=validated_data.pop('username'))
        return DomainEvent.objects.create(
            owner=owner,
            blob=blob,
            **validated_data
        )
    
    def validate_username(self, value):
        if not User.objects.filter(username=value).exists():
            raise User.DoesNotExist("Cannot find username matching '{}'".format(value))
        return value

class DomainEventReadSerializer(serializers.ModelSerializer):
    payload = serializers.SerializerMethodField()
    timestamp = serializers.SerializerMethodField()
    owner = UserSerializer()

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'owner',
            'timestamp',
            'payload',
        )
    
    def get_timestamp(self, obj):
        return obj.date_occurred

    def get_payload(self, obj):
        return json.loads(obj.blob)
