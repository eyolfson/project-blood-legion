from django.urls import path

from . import views

app_name = 'project_blood_legion'

urlpatterns = [
	path('', views.index, name='index'),
]
