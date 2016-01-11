from django.contrib import admin
from common.models import DomainEvent

class EventAdmin(admin.ModelAdmin):
	list_display = ('date_occurred', 'aggregate_id', 'aggregate_type', 'event_type', 'sequence_nr', 'username',)
	list_filter = ('username', 'aggregate_type', 'event_type')
	search_fields = ['blob']

# Register your models here.
admin.site.register(DomainEvent, EventAdmin)