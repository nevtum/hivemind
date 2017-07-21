from django.contrib import admin

from common.models import CustomFilter, DomainEvent, Manufacturer, Project


class EventAdmin(admin.ModelAdmin):
	list_display = (
        'id',
        'date_occurred',
        'aggregate_id',
        'aggregate_type',
        'event_type',
        'sequence_nr',
        'owner',
    )
	list_filter = ('owner', 'aggregate_type', 'event_type')
	search_fields = ['blob']

class ManufacturerAdmin(admin.ModelAdmin):
    list_display = ('name',)

class ProjectAdmin(admin.ModelAdmin):
    list_display = ('date_created', 'code', 'description')
    list_filter = ('manufacturer',)
    ordering = ('-date_created',)
    prepopulated_fields = { 'slug': ('code',) }

class CustomFilterAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date_created', 'date_updated')

# Register your models here.
admin.site.register(DomainEvent, EventAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(CustomFilter, CustomFilterAdmin)
