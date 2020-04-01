from django.forms import ModelForm

from .models import Loot, Note, Reserve

class LootForm(ModelForm):
	class Meta:
		model = Loot
		fields = ['item', 'boss', 'character']

class NoteForm(ModelForm):
	class Meta:
		model = Note
		fields = ['text']

class ReserveForm(ModelForm):
	class Meta:
		model = Reserve
		fields = ['item1', 'item2']
