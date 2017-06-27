import json

from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import DomainEvent


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField('get_user_full_name')

    def get_user_full_name(self, obj):
        return "{0} {1}".format(obj.first_name, obj.last_name)

class DomainEventWriteSerializer(serializers.ModelSerializer):
    payload = serializers.JSONField(source='blob')
    timestamp = serializers.DateTimeField(source='date_occurred')
    owner = UserSerializer()

    class Meta:
        model = DomainEvent
        fields = (
            'timestamp',
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'payload',
            'owner',
        )
    
    def create(self, validated_data):
        blob = json.dumps(validated_data.pop('blob'), indent=2)
        owner = User.objects.get(username=validated_data.pop('owner')['username'])
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
            'timestamp',
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'payload',
            'owner',
        )

    def get_timestamp(self, obj):
        return obj.date_occurred

    def get_payload(self, obj):
        return json.loads(obj.blob)
