from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^search/$', views.search, name='search'),
    url(r'^index/$', views.index, name='index'),
    url(r'^meta/$', views.Meta.as_view(), name='meta'),
]
