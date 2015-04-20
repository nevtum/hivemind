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
