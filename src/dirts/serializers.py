from .models import Defect, Status, Priority
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    full_name = serializers.SerializerMethodField('get_user_full_name')

    def get_user_full_name(self, obj):
        request = self.context['request']
        user = request.user
        return "{0} {1}".format(user.first_name, user.last_name)

class DefectSerializer(serializers.ModelSerializer):
    status = serializers.ReadOnlyField(source='status.name')
    priority = serializers.ReadOnlyField(source='priority.name')
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
        