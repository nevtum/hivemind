from django.shortcuts import render
from clients.services import ContactRepository

rep = ContactRepository()

def index(request):
    c = rep.all_contacts()
    return render(request, 'contacts.html', {'contacts': c})

def contacts(request, query):
    c = rep.search(query)
    return render(request, 'contacts.html', {'contacts': c})
