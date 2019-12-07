from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect
from django.urls import reverse

from .forms import LootForm
from .models import Character, Item, Raid

def index(request):
	context = {
		'title': 'Blood Legion',
	}
	return render(request, 'project_blood_legion/index.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def character_index(request):
	context = {
		'title': 'Characters',
		'characters': Character.objects.order_by('cls', 'name'),
	}
	return render(request, 'project_blood_legion/character_index.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def character_detail(request, character_id):
	character = get_object_or_404(Character, pk=character_id)
	context = {
		'title': character.name,
		'character': character,
	}
	return render(request, 'project_blood_legion/character_detail.html', context)

@login_required
@permission_required('project_blood_legion.view_item', raise_exception=True)
def item_index(request):
	context = {
		'title': 'Items',
		'items': Item.objects.all(),
	}
	return render(request, 'project_blood_legion/item_index.html', context)

@login_required
@permission_required('project_blood_legion.view_item', raise_exception=True)
def item_detail(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	context = {
		'title': item.name,
		'item': item,
	}
	return render(request, 'project_blood_legion/item_detail.html', context)

@login_required
@permission_required('project_blood_legion.view_raid', raise_exception=True)
def raid_index(request):
	context = {
		'title': 'Raids',
		'raids': Raid.objects.all(),
	}
	return render(request, 'project_blood_legion/raid_index.html', context)

@login_required
@permission_required('project_blood_legion.view_raid', raise_exception=True)
def raid_detail(request, raid_id):
	raid = get_object_or_404(Raid, pk=raid_id)
	groups = list(raid.group_set.all())
	if request.user.is_authenticated and request.user.has_perm('project_blood_legion.change_loot'):
		for group in groups:
			group.prefix = 'loot-{}'.format(group.id)
			if request.method == 'POST' and group.prefix in request.POST:
				group.loot_form = LootForm(request.POST, prefix=group.prefix)
				if group.loot_form.is_valid():
					loot = group.loot_form.save()
					loot.group = group
					loot.save()
					return HttpResponseRedirect(reverse('project_blood_legion:raid_detail', args=(raid_id,)))
			else:
				group.loot_form = LootForm(prefix=group.prefix)
	context = {
		'title': str(raid),
		'raid': raid,
		'groups': groups,
	}
	return render(request, 'project_blood_legion/raid_detail.html', context)
