from django.contrib.auth.hashers import make_password
from django.shortcuts import redirect, render
from django.views.generic import CreateView, ListView

from .forms import SignupForm
from .models import SignupRequest


class SignupRequestView(CreateView):
    model = SignupRequest
    form_class = SignupForm
    template_name = 'register.html'

    def form_valid(self, form):
        sr = form.instance
        sr.password = make_password(sr.password) # hash password
        form.save()
        return redirect('thanks')

def register_complete(request):
    return render(request, 'wait_admin.html')

class SignupListView(ListView):
    queryset = SignupRequest.objects.filter(pending_approval=True)
    context_object_name = 'registrations'
    template_name = 'registrations.html'