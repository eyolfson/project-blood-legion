from django.urls import path

from . import views

app_name = 'project_blood_legion'

urlpatterns = [
	path('', views.index, name='index'),
	path('roster/', views.roster, name='roster'),
	path('roster/alts/', views.alts, name='alts'),
	path('character/', views.character_index, name='character_index'),
	path('character/<int:character_id>/', views.character_detail, name='character_detail'),
	path('item/', views.item_index, name='item_index'),
	path('item/<int:item_id>/', views.item_detail, name='item_detail'),
	path('raid/', views.raid_index, name='raid_index'),
	path('raid/<int:raid_id>/', views.raid_detail, name='raid_detail'),
	path('loot/', views.loot_index, name='loot_index'),
	path('boss/', views.boss_index, name='boss_index'),
	path('boss/<int:boss_id>/', views.boss_detail, name='boss_detail'),
	path('question/', views.question_index, name='question_index'),
	path('question/<int:question_id>/', views.question_detail, name='question_detail'),
	path('notes/', views.note_index, name='note_index'),
]
