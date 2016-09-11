from django.shortcuts import render
from django.views.generic import ListView
from .models import Activity

class ActivityListView(ListView):
    queryset = Activity.objects.order_by('-date_occurred')
    template_name = 'feed.html'
    context_object_name = 'feed'
    paginate_by = 50