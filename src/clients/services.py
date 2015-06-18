from django.db.models import Q

from .models import Contact

class ContactRepository:
    def search(self, keyword):
        query = Q(employed_by__contains=keyword) \
        | Q(role__contains=keyword) \
        | Q(first_name__contains=keyword) \
        | Q(last_name__contains=keyword)

        return Contact.objects.filter(query)

    def all_contacts(self):
        return Contact.objects.all()
