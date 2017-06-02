from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.travel, name = 'travel'),
	url(r'^new/(?P<id>\d+)$', views.new, name = 'new'),
	url(r'^add$', views.add, name = 'add'),
	url(r'^dest/(?P<id>\d+)$', views.dest, name = 'dest'),
	url(r'^join/(?P<trip_id>\d+)$', views.join, name = 'join'),
	url(r'^delete/(?P<trip_id>\d+)$', views.delete, name = 'delete'),
]