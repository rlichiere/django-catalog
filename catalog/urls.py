from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^projects$', views.ProjectsView.as_view(), name='projects'),
    url(r'^project/(?P<pk>[0-9]+)$', views.ProjectDetailView.as_view(), name='project'),
    url(r'^participant/(?P<pk>[0-9]+)$', views.ParticipantDetailView.as_view(), name='participant'),
    url(r'^capacity/(?P<pk>[0-9]+)$', views.CapacityDetailView.as_view(), name='capacity'),
    url(r'^my$', views.MyView.as_view(), name='my'),
    url(r'^command$', views.CommandView.as_view(), name='command'),
]
