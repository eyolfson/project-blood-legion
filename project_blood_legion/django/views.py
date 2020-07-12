from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.html import escape

import markdown
from markdown.extensions.toc import TocExtension

from .forms import LootForm, NoteForm, ReserveForm
from .models import Boss, Character, Item, Raid, Note, Member, Question, Answer, Instance, Alt, Reserve

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
		'hide_rank': 3,
		'show_members': True,
		'members': Member.objects.filter(rank__lte=4).order_by('main_character__cls', 'main_character__name'),
	}
	return render(request, 'project_blood_legion/roster.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def member(request):
	context = {
		'hide_rank': 5,
		'show_members': False,
		'members': Member.objects.filter(rank=5).order_by('main_character__cls', 'main_character__name'),
	}
	return render(request, 'project_blood_legion/roster.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def alts(request):
	context = {
		'alts': Alt.objects.filter(member__rank__lte=4).order_by('character__cls', 'character__name'),
	}
	return render(request, 'project_blood_legion/alts.html', context)

@login_required
@permission_required('project_blood_legion.view_character', raise_exception=True)
def member_alts(request):
	context = {
		'alts': Alt.objects.filter(member__rank=5).order_by('character__cls', 'character__name'),
	}
	return render(request, 'project_blood_legion/alts.html', context)

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
			member = request.user.member
			if member.main_character == character:
				is_character = True
			for alt in member.alts.all():
				if alt.character == character:
					is_character = True
					break
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
	if is_character or request.user.has_perm('project_blood_legion.view_reserve'):
		reserves = list(Reserve.objects.filter(character=character))
	else:
		reserves = []

	if is_character:
		if request.method == 'POST' and 'note' in request.POST:
			note_form = NoteForm(request.POST, prefix='note')
			if note_form.is_valid():
				new_note = note_form.save(commit=False)
				if note:
					note.text = markdown.markdown(
						escape(new_note.text),
						extensions=[
							TocExtension(baselevel=3),
							'nl2br',
							'tables',
						],
						output='html5',
					)
					note.save()
				else:
					new_note.character = character
					new_note.save()
				return HttpResponseRedirect(reverse('project_blood_legion:character_detail', args=(character_id,)))
		else:
			note_form = NoteForm(prefix='note')
		for reserve in reserves:
			reserve.prefix = 'zone-{}'.format(reserve.zone.id)
			if request.method == 'POST' and reserve.prefix in request.POST:
				reserve.form = ReserveForm(request.POST, prefix=reserve.prefix)
				if reserve.form.is_valid():
					new_reserve = reserve.form.save(commit=False)
					reserve.item1 = new_reserve.item1
					reserve.item2 = new_reserve.item2
					reserve.save()
					return HttpResponseRedirect(reverse('project_blood_legion:character_detail', args=(character_id,)))
			else:
				reserve.form = ReserveForm(prefix=reserve.prefix)

	loot_set = character.loot_set.all()
	if 'by-date' in request.GET:
                loot_set = loot_set.order_by('-instance__scheduled_start')

	context = {
		'character': character,
		'loot_set': loot_set,
		'note': note,
		'note_form': note_form,
		'reserves': reserves,
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
		'bosses': Boss.objects.all(),
	}
	return render(request, 'project_blood_legion/boss_index.html', context)

@login_required
@permission_required('project_blood_legion.view_boss', raise_exception=True)
def boss_detail(request, boss_id):
	boss = get_object_or_404(Boss, pk=boss_id)
	boss_loot = boss.loot_set.filter(instance__isnull=False)
	if boss.name == 'Trash':
		from django.utils import timezone
		boss_kills = Instance.objects.filter(
			scheduled_start__lte=timezone.now(),
			raid__in=boss.zone.raid_set.all()
		).count()
	else:
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
@permission_required('project_blood_legion.view_question', raise_exception=True)
def question_index(request):
	context = {
		'questions': Question.objects.all(),
	}
	return render(request, 'project_blood_legion/question_index.html', context)

@login_required
@permission_required('project_blood_legion.view_question', raise_exception=True)
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
	if request.user.has_perm('project_blood_legion.view_answer'):
		answers = Answer.objects.filter(question=question).order_by('-choice', 'member__main_character__cls', 'member__main_character__name')
		context['answers'] = answers
	return render(request, 'project_blood_legion/question_detail.html', context)
