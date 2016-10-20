from django.contrib import admin
from .models import SignupRequest

class RegistrationsAdmin(admin.ModelAdmin):
	list_display = ('date_submitted', 'username', 'email', 'pending_approval',)

admin.site.register(SignupRequest, RegistrationsAdmin)
