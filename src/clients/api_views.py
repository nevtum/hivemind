from clients.models import Company, Contact, WorkRole
from rest_framework import viewsets, generics
from clients import serializers

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = serializers.CompanySerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = serializers.ContactSerializer

class WorkRoleViewSet(viewsets.ModelViewSet):
    queryset = WorkRole.objects.all()
    serializer_class = serializers.WorkRoleSerializer

class CompanyContactList(generics.ListAPIView):
    serializer_class = serializers.ContactSerializer

    def get_queryset(self):
        code = self.kwargs['code']
        return Contact.objects.filter(company=code)
