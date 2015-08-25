from .models import Defect
from rest_framework import serializers

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = ('id',
        'date_created',
        'status',
        'project_code',
        'release_id',
        'priority',
        'reference',
        # 'description',
        # 'comments',
        'submitter')
