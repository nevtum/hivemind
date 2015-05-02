from django.shortcuts import render
from clients.models import Company, Contact

# Create your views here.
def index(request):
    c = Company.objects.all()
    return render(request, 'index.html', {'companies': c})

def contacts(request, code):
    c = Contact.objects.filter(company=code)
    return render(request, 'contacts.html', {'contacts': c})

def create_company(request):
    if request.method == 'GET':
        return render(request, 'create_company.html')

    # else 'POST'

from rest_framework import viewsets
from clients.serializers import CompanySerializer, ContactSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
