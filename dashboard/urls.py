from django.conf.urls import url
from .import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^stdbscan_input/$', views.stdbscan_input, name='stdbscan_input'),
	url(r'^stdbscan_dashboard/$', views.stdbscan_dashboard, name='stdbscan_dashboard'),
	url(r'^stdbscan_charts/$', views.stdbscan_charts, name='stdbscan_charts'),
	url(r'^stdbscan_table/$', views.stdbscan_table, name='stdbscan_table'),
	url(r'^kmeans_input/$', views.kmeans_input, name='kmeans_input'),
	url(r'^kmeans_dashboard/$', views.kmeans_dashboard, name='kmeans_dashboard'),
	url(r'^kmeans_charts/$', views.kmeans_charts, name='kmeans_charts'),
	url(r'^kmeans_table/$', views.kmeans_table, name='kmeans_table'),
	url(r'^choose_algo/$', views.choose_algo, name='choose_algo'),
	url(r'^menu/$', views.menu, name='menu')
]

