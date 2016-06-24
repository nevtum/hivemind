from .models import Defect, Status, Priority
from rest_framework import serializers

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('name',)

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ('name',)

class UserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=100)

class DefectSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    priority = PrioritySerializer()
    submitter = UserSerializer()

    class Meta:
        model = Defect
        fields = (
            'id',
            'date_created',
            'date_changed',
            'status',
            'project_code',
            'release_id',
            'priority',
            'reference',
            'submitter'
        )
        