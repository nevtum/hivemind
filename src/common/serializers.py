from .models import DomainEvent
from rest_framework import serializers

class DomainEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'event_type',
            'blob',
            'date_occurred',
            'username'
            )