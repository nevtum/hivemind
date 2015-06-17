from django.shortcuts import render
from clients.models import Contact

def index(request):
    c = Contact.objects.all()
    return render(request, 'contacts.html', {'contacts': c})

def contacts(request, query):
    c = Contact.objects.filter(employed_by__contains=query)
    return render(request, 'contacts.html', {'contacts': c})
