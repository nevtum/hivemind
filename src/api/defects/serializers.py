from rest_framework import serializers
from django.contrib.auth.models import User

from common.models import Project
from ..core.serializers import UserSerializer
from dirts.models import Defect, Priority, Status

class PrioritySerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return obj.name
        
    class Meta:
        model = Priority

class StatusSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        return obj.name

    class Meta:
        model = Status

class ProjectSuggestionSerializer(serializers.Serializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_label(self, obj):
        return "{} - {}".format(obj.code, obj.description)
    
    def get_value(self, obj):
        return obj.code

    class Meta:
        model = Project

class DefectSuggestionSerializer(serializers.Serializer):
    label = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    def get_label(self, obj):
        return obj.reference
    
    def get_value(self, obj):
        return obj.reference

    class Meta:
        model = Defect

class DefectDetailSerializer(serializers.ModelSerializer):
    def to_representation(self, obj):
        repr = super(DefectDetailSerializer, self).to_representation(obj)
        repr['history'] = []
        repr['more_like_this'] = []
        return repr

    status = serializers.ReadOnlyField(source='status.name')
    priority = serializers.ReadOnlyField(source='priority.name')
    submitter = UserSerializer()
    class Meta:
        model = Defect
        fields = (
            'project_code',
            'date_created',
            'date_changed',
            'release_id',
            'status',
            'priority',
            'reference',
            'description',
            'submitter',
            'comments',
        )

class CreateDefectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    priority = serializers.CharField(max_length=20)

    def create(self, validated_data):
        priority = Priority.objects.get(name=validated_data.pop('priority'))
        return Defect.objects.create(priority=priority, **validated_data)

    class Meta:
        model = Defect
        fields = (
            'id',
            'project_code',
            'release_id',
            'status',
            'priority',
            'reference',
            'description',
            'comments',
        )

class DefectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    priority = serializers.ReadOnlyField(source='priority.name')
    detail = serializers.HyperlinkedRelatedField(source='id', view_name='api:defects:all-detail', read_only=True)    
    submitter = UserSerializer()

    class Meta:
        model = Defect
        fields = (
            'id',
            'detail',
            'date_created',
            'date_changed',
            'status',
            'project_code',
            'release_id',
            'priority',
            'reference',
            'submitter'
        )

class MoreLikeThisSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    link = serializers.HyperlinkedRelatedField(source='id', view_name='api:defectssimilar-defects', read_only=True)
    reference = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    created_by = serializers.ReadOnlyField(source='submitter.username')

    class Meta:
        model = Defect
        fields = (
            'id',
            'reference',
            'date_created'
            'created_by'
        )
