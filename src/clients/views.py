from django.shortcuts import render
from clients.services import ContactRepository

rep = ContactRepository()

def contacts(request):
    search_param = _get_search_parameters(request)
    c = rep.search(search_param)
    return render(request, 'contacts.html', {'contacts': c})

def _get_search_parameters(request):
    query = request.GET.get('search')
    print(query)
    if query is None:
        return ''
    return query
