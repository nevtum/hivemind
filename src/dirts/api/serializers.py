from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Defect, Priority, Status

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

class SuggestionSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField('get_user_full_name')

    def get_user_full_name(self, obj):
        request = self.context['request']
        user = request.user
        return "{0} {1}".format(user.first_name, user.last_name)

class CreateDefectSerializer(serializers.ModelSerializer):
    priority = serializers.CharField(max_length=20)

    def create(self, validated_data):
        priority = Priority.objects.get(name=validated_data.pop('priority'))
        return Defect(priority=priority, **validated_data)

    class Meta:
        model = Defect
        fields = (
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
    detail = serializers.HyperlinkedRelatedField(source='id', view_name='defects:api:all-detail', read_only=True)    
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
    link = serializers.HyperlinkedRelatedField(source='id', view_name='defects:api:similar-defects', read_only=True)
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
