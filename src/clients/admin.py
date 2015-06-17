from django.contrib import admin
from clients.models import Contact, Jurisdiction, RecommendationSubscription

# Register your models here.
admin.site.register(Contact)
admin.site.register(Jurisdiction)
admin.site.register(RecommendationSubscription)
