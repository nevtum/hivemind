from django.db.models import Q

from clients.models import Contact

def search(keyword):
    query = Q(employed_by__contains=keyword) \
    | Q(role__contains=keyword) \
    | Q(first_name__contains=keyword) \
    | Q(last_name__contains=keyword)
    return Contact.objects.filter(query)

def all_contacts():
    return Contact.objects.all()
