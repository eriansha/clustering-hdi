from django.conf.urls import url
from .import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^parameters/$', views.parameters_list, name='parameters_list'),
	url(r'^parameters/add/$', views.parameters_add, name='parameters_add'),
]

