from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required

from .models import Character, Item, Raid

def index(request):
	context = {
		'title': 'Blood Legion',
	}
	return render(request, 'project_blood_legion/index.html', context)

@permission_required('project_blood_legion.view_character')
def character_index(request):
	context = {
		'title': 'Characters',
		'characters': Character.objects.all(),
	}
	return render(request, 'project_blood_legion/character_index.html', context)

@permission_required('project_blood_legion.view_character')
def character_detail(request, character_id):
	character = get_object_or_404(Character, pk=character_id)
	context = {
		'title': character.name,
		'character': character,
	}
	return render(request, 'project_blood_legion/character_detail.html', context)

@permission_required('project_blood_legion.view_character')
def item_index(request):
	context = {
		'title': 'Items',
		'items': Item.objects.all(),
	}
	return render(request, 'project_blood_legion/item_index.html', context)

@permission_required('project_blood_legion.view_character')
def item_detail(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	context = {
		'title': item.name,
		'item': item,
	}
	return render(request, 'project_blood_legion/item_detail.html', context)

@permission_required('project_blood_legion.view_character')
def raid_index(request):
	context = {
		'title': 'Raids',
		'raids': Raid.objects.all(),
	}
	return render(request, 'project_blood_legion/raid_index.html', context)

@permission_required('project_blood_legion.view_character')
def raid_detail(request, raid_id):
	raid = get_object_or_404(Raid, pk=raid_id)
	context = {
		'title': str(raid),
		'raid': raid,
	}
	return render(request, 'project_blood_legion/raid_detail.html', context)
