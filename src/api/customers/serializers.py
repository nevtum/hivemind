from django.contrib.auth.models import User
from rest_framework import serializers

from common.models import Manufacturer, Project

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