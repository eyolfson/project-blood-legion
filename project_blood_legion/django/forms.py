from django.db.models import Q
from django.forms import ModelForm

from .models import Character, Item, Loot, Note, Reserve

class LootForm(ModelForm):
	def __init__(self, boss, *args, **kwargs):
		super().__init__(*args, **kwargs)

		self.boss = boss
		self.fields['character'].queryset = Character.objects.filter(
			Q(member__rank__lte=4) | Q(alt__member__rank__lte=4)
		)
		self.fields['item'].queryset = Item.objects.filter(boss=boss)

	class Meta:
		model = Loot
		fields = ['item', 'character']

class NoteForm(ModelForm):
	class Meta:
		model = Note
		fields = ['text']

class ReserveForm(ModelForm):
	class Meta:
		model = Reserve
		fields = ['item1', 'item2']
