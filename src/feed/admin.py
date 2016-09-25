from django.contrib import admin
from .models import Activity

class ActivityAdmin(admin.ModelAdmin):
    list_display = ('date_occurred', 'project', 'summary', 'submitter',)

# Register your models here.
admin.site.register(Activity, ActivityAdmin)