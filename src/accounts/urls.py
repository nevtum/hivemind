from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^register/$', views.SignupRequestView.as_view(), name='register'),
    url(r'^completed/$', views.register_complete, name='thanks'),
    url(r'^requests_pending/$', views.SignupListView.as_view(), name='pending'),    
    url(r'^approve_registration/(?P<pk>\d+?)$', views.approve_registration, name='approve'),    
    url(r'^reject_registration/(?P<pk>\d+?)$', views.reject_registration, name='reject'),    
]