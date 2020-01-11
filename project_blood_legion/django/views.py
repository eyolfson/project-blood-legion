from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import LootForm, NoteForm
from .models import Boss, Character, Item, Raid, Note, Member, Question, Answer

def get_member_or_deny(request):
	try:
		return request.user.member
	except Member.DoesNotExist:
		pass
	raise PermissionDenied

def index(request):
	return render(request, 'project_blood_legion/index.html', {})

def roster(request):
	context = {
		'members': Member.objects.filter(rank__lte=4).order_by('main_character__cls', 'main_character__name'),
	}
	return render(request, 'project_blood_legion/roster.html', context)

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

	is_character = False
	can_view = False
	if request.user.is_authenticated:
		try:
			is_character = request.user.member.main_character == character
		except Member.DoesNotExist:
			pass
		can_view = request.user.has_perm('project_blood_legion.view_note')

	note = None
	if is_character or can_view:
		try:
			note = character.note
		except Note.DoesNotExist:
			note = None

	note_form = None
	if is_character:
		if request.method == 'POST':
			note_form = NoteForm(request.POST)
			if note_form.is_valid():
				new_note = note_form.save(commit=False)
				if note:
					note.text = new_note.text
					note.save()
				else:
					new_note.character = character
					new_note.save()
				return HttpResponseRedirect(reverse('project_blood_legion:character_detail', args=(character_id,)))
		else:
			note_form = NoteForm()

	context = {
		'character': character,
		'note': note,
		'note_form': note_form,
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
		'raids': Raid.objects.order_by('-start').annotate(instance_count=Count('instance')).filter(instance_count__gte=1),
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

@login_required
@permission_required('project_blood_legion.view_boss', raise_exception=True)
def boss_index(request):
	context = {
		'bosses': Boss.objects.exclude(name='Trash'),
	}
	return render(request, 'project_blood_legion/boss_index.html', context)

@login_required
@permission_required('project_blood_legion.view_boss', raise_exception=True)
def boss_detail(request, boss_id):
	boss = get_object_or_404(Boss, pk=boss_id)
	if boss.name == 'Trash':
		raise Http404
	boss_loot = boss.loot_set.filter(instance__isnull=False)
	boss_kills = boss_loot.order_by('instance').values('instance').distinct().count()
	boss_drops = list(boss_loot.order_by('item').values('item').distinct().annotate(count=Count('item')).order_by('-count', 'item'))
	for drop in boss_drops:
		drop['item'] = Item.objects.get(id=drop['item'])
		drop['percentage'] = '{:.0%}'.format(drop['count'] / boss_kills)
	context = {
		'boss': boss,
		'boss_kills': boss_kills,
		'boss_drops': boss_drops,
	}
	return render(request, 'project_blood_legion/boss_detail.html', context)

@login_required
def question_index(request):
	member = get_member_or_deny(request)
	context = {
		'questions': Question.objects.all(),
		'member': member,
	}
	return render(request, 'project_blood_legion/question_index.html', context)

@login_required
def question_detail(request, question_id):
	member = get_member_or_deny(request)
	question = get_object_or_404(Question, pk=question_id)
	answer = None
	try:
		answer = Answer.objects.get(question=question, member=member)
	except Answer.DoesNotExist:
		pass

	if request.method == 'POST' and 'choice' in request.POST:
		if answer is None:
			answer = Answer.objects.create(question=question, member=member, choice=False)
		if request.POST['choice'] == 'Yes':
			answer.choice = True
		elif request.POST['choice'] == 'No':
			answer.choice = False
		answer.save()
		return HttpResponseRedirect(reverse('project_blood_legion:question_detail', args=(question_id,)))

	context = {
		'question': question,
		'answer': answer,
	}
	if member.is_officer():
		answers = Answer.objects.filter(question=question).order_by('choice', 'member__main_character__cls', 'member__main_character__name')
		context['answers'] = answers
	return render(request, 'project_blood_legion/question_detail.html', context)
