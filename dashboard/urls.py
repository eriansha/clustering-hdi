from django.conf.urls import url
from .import views

app_name = 'dashboard'

urlpatterns = [
	url(r'^dashboard/$', views.dashboard, name='dashboard'),
	url(r'^input/$', views.input_param, name='input'),
]

