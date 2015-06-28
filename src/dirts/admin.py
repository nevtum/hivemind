from django.contrib import admin
from dirts.models import Status, Priority, Defect, DefectHistoryItem

# Register your models here.
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Defect)
admin.site.register(DefectHistoryItem)
