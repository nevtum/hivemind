from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register/$', views.SignupRequestView.as_view(), name='register'),
    url(r'^completed/$', views.register_complete, name='thanks'),
]