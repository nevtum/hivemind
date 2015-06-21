from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from dirts.models import Defect
from dirts.services import dirt_manager

# Create your views here.

def index(request):
    defects = Defect.objects.all().order_by('-date_created')
    return render(request, 'dirt_list.html', {'defects': defects})

@login_required(login_url='/login/')
def create(request):
    if request.method == 'GET':
        return render(request, 'create.html')

    # otherwise post
    args = {
        'submitter': request.user,
        'date_created': datetime.utcnow(),
    }

    dirt_manager.raise_dirt(kwargs=args)
    return redirect('dirts-landing-url')
