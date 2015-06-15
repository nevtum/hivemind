from django.contrib import admin
from clients.models import (Company, Contact, WorkRole,
Regulator, RecommendationSubscription)

# Register your models here.
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(WorkRole)
admin.site.register(Regulator)
admin.site.register(RecommendationSubscription)
