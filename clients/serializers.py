from clients.models import Company, Contact, WorkRole
from rest_framework import serializers

class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'code', 'status')

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id',
        'company',
        'title',
        'role',
        'email',
        'first_name',
        'last_name')

class WorkRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkRole
        fields = ('name', 'department')
