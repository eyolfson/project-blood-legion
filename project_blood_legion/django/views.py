from django.shortcuts import render

from .models import Character

def index(request):
	context = {
		'title': 'Blood Legion',
		'characters': Character.objects.all(),
	}
	return render(request, 'project_blood_legion/index.html', context)
