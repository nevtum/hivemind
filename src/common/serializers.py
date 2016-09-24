from .models import DomainEvent
from rest_framework import serializers

class DomainEventSerializer(serializers.ModelSerializer):
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        return obj['payload']

    class Meta:
        model = DomainEvent
        fields = (
            'sequence_nr',
            'aggregate_id',
            'aggregate_type',
            'event_type',
            'date_occurred',
            'data',
        )
            