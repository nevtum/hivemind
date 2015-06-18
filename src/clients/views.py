from django.shortcuts import render
from clients.services import contact_repository

def contacts(request):
    search_param = _extract_search_parameters(request)
    c = contact_repository.search(search_param)
    return render(request, 'contacts.html', {'contacts': c})

def _extract_search_parameters(request):
    query = request.GET.get('search')
    if query:
        return query
    return ''
