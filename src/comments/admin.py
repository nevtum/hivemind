from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
	list_display = ('timestamp', 'id', 'author',)
	list_filter = ('author',)
	search_fields = ['content']

admin.site.register(Comment, CommentAdmin)