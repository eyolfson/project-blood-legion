from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import LootForm
from .models import Character, Item, Raid

def index(request):
	return render(request, 'project_blood_legion/index.html', {})

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def character_index(request):
	context = {
		'characters': Character.objects.order_by('cls', 'name'),
	}
	return render(request, 'project_blood_legion/character_index.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def character_detail(request, character_id):
	character = get_object_or_404(Character, pk=character_id)
	context = {
		'character': character,
	}
	return render(request, 'project_blood_legion/character_detail.html', context)

@login_required
@permission_required('project_blood_legion.view_item', raise_exception=True)
def item_index(request):
	context = {
		'items': Item.objects.all(),
	}
	return render(request, 'project_blood_legion/item_index.html', context)

@login_required
@permission_required('project_blood_legion.view_item', raise_exception=True)
def item_detail(request, item_id):
	item = get_object_or_404(Item, pk=item_id)
	context = {
		'item': item,
	}
	return render(request, 'project_blood_legion/item_detail.html', context)

@login_required
@permission_required('project_blood_legion.view_raid', raise_exception=True)
def raid_index(request):
	context = {
		'raids': Raid.objects.annotate(instance_count=Count('instance')).filter(instance_count__gte=1),
	}
	return render(request, 'project_blood_legion/raid_index.html', context)

@login_required
@permission_required('project_blood_legion.view_raid', raise_exception=True)
def raid_detail(request, raid_id):
	raid = get_object_or_404(Raid, pk=raid_id)
	instances = list(raid.instance_set.all())
	if request.user.is_authenticated and request.user.has_perm('project_blood_legion.change_loot'):
		for instance in instances:
			instance.prefix = 'loot-{}'.format(instance.id)
			if request.method == 'POST' and instance.prefix in request.POST:
				instance.loot_form = LootForm(request.POST, prefix=instance.prefix)
				if instance.loot_form.is_valid():
					loot = instance.loot_form.save()
					loot.instance = instance
					loot.save()
					return HttpResponseRedirect(reverse('project_blood_legion:raid_detail', args=(raid_id,)))
			else:
				instance.loot_form = LootForm(prefix=instance.prefix)
	context = {
		'raid': raid,
		'instances': instances,
	}
	return render(request, 'project_blood_legion/raid_detail.html', context)
