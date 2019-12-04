from django.db import models
from django.conf import settings

class Character(models.Model):
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
		null=True,
	)
	name = models.CharField(
		max_length=100,
		unique=True,
	)
	guid = models.IntegerField(
		null=True,
	)

	def __str__(self):
		return self.name

	class Meta:
		db_table = '"project_blood_legion_character"'
		ordering = ['name']

class Item(models.Model):
	POOR = 'P'
	COMMON = 'C'
	UNCOMMON = 'U'
	RARE = 'R'
	EPIC = 'E'
	LEGENDARY = 'L'
	ARTIFACT = 'A'
	QUALITY_CHOICES = [
		(POOR, 'Poor'),
		(COMMON, 'Common'),
		(UNCOMMON, 'Uncommon'),
		(RARE, 'Rare'),
		(EPIC, 'Epic'),
		(LEGENDARY, 'Legendary'),
		(ARTIFACT, 'Artifact'),
	]

	name = models.CharField(
		max_length=100,
		unique=True,
	)
	quality = models.CharField(max_length=1, choices=QUALITY_CHOICES)
	classicdb_id = models.IntegerField()

	def __str__(self):
		return self.name

	class Meta:
		db_table = '"project_blood_legion_item"'
		ordering = ['name']
