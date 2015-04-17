from django.shortcuts import render
from clients.models import Company, Contact

# Create your views here.

def index(request):
    c = Company.objects.all()
    return render(request, 'index.html', {'companies': c})
