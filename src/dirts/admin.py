from django.contrib import admin
from dirts.models import Status, Priority, Defect, DefectHistoryItem

class DefectAdmin(admin.ModelAdmin):
	list_display = ('date_created', 'date_changed', 'project_code', 'release_id', 'submitter', 'status',)
	list_filter = ('priority', 'status',)
	search_fields = ['project_code', 'reference', 'description', 'comments']

# Register your models here.
admin.site.register(Status)
admin.site.register(Priority)
admin.site.register(Defect, DefectAdmin)
admin.site.register(DefectHistoryItem)