from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import permission_required

from .models import Character, Item

def index(request):
	context = {
		'title': 'Blood Legion',
	}
	return render(request, 'project_blood_legion/index.html', context)

@permission_required('polls.view_character')
def character_index(request):
	context = {
		'title': 'Characters',
		'characters': Character.objects.all(),
	}
	return render(request, 'project_blood_legion/character_index.html', context)

@permission_required('polls.view_character')
def character_detail(request, character_id):
	character = get_object_or_404(Character, pk=character_id)
	context = {
		'title': character.name,
		'character': character,
	}
	return render(request, 'project_blood_legion/character_detail.html', context)
