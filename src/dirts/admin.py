from django.contrib import admin
from dirts.models import Status, Severity, Defect

# Register your models here.
admin.site.register(Status)
admin.site.register(Severity)
admin.site.register(Defect)
