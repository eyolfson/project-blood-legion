from django.urls import path

from . import views

app_name = 'project_blood_legion'

urlpatterns = [
	path('', views.index, name='index'),
	path('character/', views.character_index, name='character_index'),
	path('character/<int:character_id>/', views.character_detail, name='character_detail'),
]
