from django.conf.urls import url, include
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^display/(?P<ticker>[A-Z]{1,5})', views.display, name='display'),
	url(r'^keyStats/(?P<ticker>[A-Z]{1,5})', views.keyStats, name='keyStats'),
	url(r'^charts/(?P<ticker>[A-Z]{1,5})', views.charts, name='charts'),
	url(r'^indices/', views.stockIndexes, name='stockIndexes'),
	url(r'^compare/', views.stockCompare, name='stockCompare'),
	url(r'^customStats/(?P<ticker>[A-Z]{1,5})', views.customStats, name='customStats'),
]
