from django.forms import ModelForm

from .models import Loot, Note

class LootForm(ModelForm):
	class Meta:
		model = Loot
		fields = ['item', 'boss', 'character']

class NoteForm(ModelForm):
	class Meta:
		model = Note
		fields = ['text']
