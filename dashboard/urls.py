from django.conf.urls import url
from .import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^charts/$', views.charts, name='charts'),
	url(r'^result_table/$', views.result_table, name='result_table'),
	url(r'^input/$', views.input_param, name='input'),
	url(r'^menu/$', views.menu, name='menu')
]

