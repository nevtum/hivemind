from django.contrib import admin
from common.models import DomainEvent, Manufacturer, Project

class EventAdmin(admin.ModelAdmin):
	list_display = (
        'id',
        'date_occurred',
        'aggregate_id',
        'aggregate_type',
        'event_type',
        'sequence_nr',
        'username',
    )
	list_filter = ('username', 'aggregate_type', 'event_type')
	search_fields = ['blob']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'code', 'description')
    list_filter = ('manufacturer',)
    ordering = ('-date_created',)
    prepopulated_fields = { 'slug': ('code',) }

# Register your models here.
admin.site.register(DomainEvent, EventAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Project, ProjectAdmin)