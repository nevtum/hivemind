from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required as auth
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register(r'all', views.DefectBaseViewSet, 'all')
router.register(r'active', views.DefectActiveViewSet, 'active')
router.register(r'recent', views.RecentlyChangedDefectViewSet, 'recent')
router.register(r'status_list', views.StatusViewSet)
router.register(r'priority_list', views.PriorityViewSet)
router.register(r'suggest_defects', views.AutoCompleteDefectTitles, 'suggest')
router.register(r'suggest_projects', views.AutoCompleteProjects, 'project-suggest')
router.register(r'defect_activities', views.DefectActivitiesForProject, 'activities')


urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^new_defect/$', views.CreateDefectView.as_view(), name='create'),
    url(r'^more_like_this/(?P<pk>\d+?)/$', views.more_like_this_defect, name='similar-defects'),
]
