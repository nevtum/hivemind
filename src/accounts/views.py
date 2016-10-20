from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .models import SignupRequest

class SignupRequestView(CreateView):
    model = SignupRequest
    fields = (
        'username',
        'email'
    )
    template_name = 'register.html'

def register(request):
    if request.method == 'POST':
        return redirect('thanks')

    return render(request, 'register.html')

def register_complete(request):
    return render(request, 'wait_admin.html')
