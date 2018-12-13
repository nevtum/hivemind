from rest_framework import serializers
from django.contrib.auth.models import User

from ..models import Defect, Priority, Status

DT_INPUT_FORMATS = [
    'iso-8601',
    '%d/%m/%Y',
    '%d/%m/%y'
]

class ImportDefectSerializer(serializers.ModelSerializer):
    date_created = serializers.DateTimeField(
        format='%d/%m/%Y',
        input_formats=DT_INPUT_FORMATS)
    date_changed = serializers.DateTimeField(
        required=False, allow_null=True,
        format='%d/%m/%Y',
        input_formats=DT_INPUT_FORMATS)
    status = serializers.SlugRelatedField(slug_field='name', queryset=Status.objects.all())
    priority = serializers.SlugRelatedField(slug_field='name', queryset=Priority.objects.all())
    submitter = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())
    class Meta:
        model = Defect
        fields = (
            'id',
            'description',
            'date_created',
            'date_changed',
            'status',
            'project_code',
            'release_id',
            'priority',
            'reference',
            'submitter'
        )
    
    def validate(self, data):
        if 'date_changed' in data and data['date_changed'] != None:
            if data['date_changed'] < data['date_created']:
                raise serializers.ValidationError("date_changed < date_created")
        else:
            if data['status'].name.lower() == 'closed':
                raise serializers.ValidationError("Date must be provided when Closed!")

        return super(ImportDefectSerializer, self).validate(data)
    
    def create(self, validated_data):
        return Defect.objects.create(**validated_data)