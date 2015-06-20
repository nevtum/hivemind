from django.shortcuts import render
from dirts.models import Defect

# Create your views here.

def index(request):
    defects = Defect.objects.all().order_by('-date_created')
    return render(request, 'dirt_list.html', {'defects': defects})
