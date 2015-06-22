from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from dirts.models import Defect, Status
from dirts.services import dirt_manager
from dirts.forms import CreateDirtForm

# Create your views here.

def index(request):
    defects = Defect.objects.all().order_by('-date_created')
    return render(request, 'dirt_list.html', {'defects': defects})

@login_required(login_url='/login/')
def create(request):
    if request.method == 'GET':
        form = CreateDirtForm()
        return render(request, 'create.html', {'form': form})

    # otherwise post
    args = {
        'project_code': request.POST['project_code'],
        'date_created': datetime.utcnow(),
        'submitter': request.user,
        'status': Status.objects.get(id=1),
        'release_id': request.POST['release_id'],
        'title': request.POST['title'],
        'description': request.POST['description'],
        'reference': request.POST['reference'],
    }

    dirt_manager.raise_dirt(**args)
    return redirect('dirts-landing-url')
