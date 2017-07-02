from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^projects$', views.ProjectsView.as_view(), name='projects'),
    url(r'^project/(?P<pk>[0-9]+)$', views.ProjectDetailView.as_view(), name='project'),
    url(r'^participant/(?P<pk>[0-9]+)$', views.ParticipantDetailView.as_view(), name='participant'),
    url(r'^capacity/(?P<pk>[0-9]+)$', views.CapacityDetailView.as_view(), name='capacity'),
    url(r'^catalog/$', views.CatalogView.as_view(), name='catalog'),
    url(r'^catalog/actor/(?P<pk>[0-9]+)$', views.CatalogActorView.as_view(), name='actor'),
    url(r'^catalog/decor/(?P<pk>[0-9]+)$', views.CatalogDecorView.as_view(), name='decor'),
    url(r'^catalog/accessory/(?P<pk>[0-9]+)$', views.CatalogAccessoryView.as_view(), name='accessory'),
    url(r'^catalog/location/(?P<pk>[0-9]+)$', views.CatalogLocationView.as_view(), name='location'),
    url(r'^my$', views.MyView.as_view(), name='my'),
    url(r'^command$', views.CommandView.as_view(), name='command'),
]
