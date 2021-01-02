from django.db import models
from django.conf import settings
from django.contrib import admin

class Character(models.Model):
	DRUID = 'DR'
	HUNTER = 'HU'
	MAGE = 'MA'
	PALADIN = 'PA'
	PRIEST = 'PR'
	ROGUE = 'RO'
	SHAMAN = 'SH'
	WARLOCK = 'WL'
	WARRIOR = 'WR'
	CLS_CHOICES = [
		(DRUID, 'Druid'),
		(HUNTER, 'Hunter'),
		(MAGE, 'Mage'),
		(PALADIN, 'Paladin'),
		(PRIEST, 'Priest'),
		(ROGUE, 'Rogue'),
		(SHAMAN, 'Shaman'),
		(WARLOCK, 'Warlock'),
		(WARRIOR, 'Warrior'),
	]

	DWARF = 'DW'
	GNOME = 'GN'
	HUMAN = 'HU'
	NIGHT_ELF = 'NE'
	ORC = 'OR'
	TAUREN = 'TA'
	TROLL = 'TR'
	UNDEAD = 'UD'
	RACE_CHOICES = [
		(DWARF, 'Dwarf'),
		(GNOME, 'Gnome'),
		(HUMAN, 'Human'),
		(NIGHT_ELF, 'Night Elf'),
		(ORC, 'Orc'),
		(TAUREN, 'Tauren'),
		(TROLL, 'Troll'),
		(UNDEAD, 'Undead'),
	]

	name = models.CharField(
		max_length=100,
		unique=True,
	)
	cls = models.CharField(max_length=2, choices=CLS_CHOICES)
	race = models.CharField(max_length=2, choices=RACE_CHOICES)
	items = models.ManyToManyField('Item', through='Loot')

	def __str__(self):
		return self.name

	class Meta:
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
	)
	quality = models.CharField(max_length=1, choices=QUALITY_CHOICES)
	classic_item_id = models.IntegerField()
	classicdb_item_id_suffix = models.CharField(max_length=8,
	                                            blank=True,
	                                            null=False)

	def __str__(self):
		if self.classic_item_id == 18563:
			return 'Bindings of the Windseeker (Left)'
		elif self.classic_item_id == 18564:
			return 'Bindings of the Windseeker (Right)'
		return self.name

	def get_rel(self):
		return '{}{}'.format(
			self.classic_item_id,
			self.classicdb_item_id_suffix
		)

	def get_url(self):
		return 'https://classicdb.ch/?item={}'.format(
			self.get_rel,
		)

	def ordered_loot(self):
                return self.loot_set.order_by('instance__scheduled_start', 'character')

	class Meta:
		ordering = ['name']

class Zone(models.Model):
	name = models.CharField(
		max_length=100,
		unique=True,
	)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']

class Boss(models.Model):
	zone = models.ForeignKey(
		Zone,
		on_delete=models.CASCADE,
		related_name='bosses',
	)
	name = models.CharField(
		max_length=100,
	)
	items = models.ManyToManyField(
		Item,
		blank=True,
		db_table='project_blood_legion_boss_items',
	)

	def __str__(self):
		if self.name == 'Trash':
			return '{} Trash'.format(self.zone)
		return self.name

	class Meta:
		ordering = ['-zone__id', 'id']
		verbose_name = 'boss'
		verbose_name_plural = 'bosses'
		unique_together = ['zone', 'name']

class Raid(models.Model):
	zone = models.ForeignKey(
		Zone,
		on_delete=models.CASCADE,
	)
	reset = models.IntegerField()
	start = models.DateTimeField()
	end = models.DateTimeField()

	def __str__(self):
		return '{} (Reset {})'.format(self.zone, self.reset)

	def ordered_loot(self):
                return self.loot_set.order_by('boss__id', 'character')

	def uninstanced_ordered_loot(self):
                return self.loot_set.filter(instance=None).order_by('boss__id', 'character')

	class Meta:
		ordering = ['zone', 'reset']
		unique_together = ['zone', 'reset']

class Instance(models.Model):
	raid = models.ForeignKey(
		Raid,
		on_delete=models.CASCADE,
	)
	name = models.CharField(
		max_length=100,
	)
	characters = models.ManyToManyField(
		Character,
		blank=True,
	)
	scheduled_start = models.DateTimeField()

	def ordered_characters(self):
                return self.characters.order_by('cls', 'name')

	def __str__(self):
		return '{} → {}'.format(self.name, self.raid)

	def ordered_loot(self):
                return self.loot_set.order_by('boss__id', 'character')

	class Meta:
		ordering = ['raid', 'name']
		unique_together = ['raid', 'name']

class Loot(models.Model):
	character = models.ForeignKey(
		Character,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	item = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
	)
	raid = models.ForeignKey(
		Raid,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	instance = models.ForeignKey(
		Instance,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	boss = models.ForeignKey(
		Boss,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)

	def __str__(self):
		return '{} → {}'.format(self.item, self.character)

	class Meta:
		verbose_name = 'loot'
		verbose_name_plural = 'loot'
		ordering = ['character', 'item']

class LootAdmin(admin.ModelAdmin):
	list_display = ('item', 'character', 'instance', 'raid', 'boss')

class Member(models.Model):
	RANK_CHOICES = [
		(1, 'Leader'),
		(2, 'Officer'),
		(3, 'Raider'),
		(4, 'Trial'),
		(5, 'Member'),
		(6, 'Friend'),
		(7, 'Retired'),
	]

	user = models.OneToOneField(
		settings.AUTH_USER_MODEL,
		on_delete=models.CASCADE,
	)
	main_character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)
	rank = models.PositiveSmallIntegerField(
		choices=RANK_CHOICES,
	)

	def __str__(self):
		return '{} ({})'.format(self.main_character, self.user)

	class Meta:
		ordering = ['main_character']

class Alt(models.Model):
	member = models.ForeignKey(
		Member,
		on_delete=models.CASCADE,
		related_name='alts',
	)
	character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return '{} ({})'.format(self.character, self.member.main_character)

class Note(models.Model):
	character = models.OneToOneField(
		Character,
		on_delete=models.CASCADE,
	)
	text = models.TextField()

	last_updated = models.DateTimeField(auto_now_add=True, null=True, blank=True)

	def __str__(self):
		return '{}'.format(self.character)

	class Meta:
		ordering = ['character']

class Question(models.Model):
	title = models.CharField(max_length=120)
	body = models.TextField()

	def __str__(self):
		return self.title

class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice = models.BooleanField()
	member = models.ForeignKey(
		Member,
		on_delete=models.CASCADE,
	)

	def __str__(self):
		return '{} → {}'.format(self.question, self.member)

class Reserve(models.Model):
	character = models.ForeignKey(
		Character,
		on_delete=models.CASCADE,
	)
	zone = models.ForeignKey(
		Zone,
		on_delete=models.CASCADE,
	)
	item1 = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name='reserve1',
	)
	item2 = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name='reserve2',
	)

	def __str__(self):
		return '{} ({})'.format(self.character, self.zone)

	class Meta:
		ordering = ['character', 'zone']
		unique_together = ['character', 'zone']

class InstanceReserveManager(models.Manager):

	def order_by_item1(self):
		return self.order_by('item1')

	def order_by_item2(self):
		return self.order_by('item2')

class InstanceReserve(models.Model):
	character = models.ForeignKey(
		Character,
		on_delete=models.CASCADE,
	)
	instance = models.ForeignKey(
		Instance,
		on_delete=models.CASCADE,
		related_name='reserves',
	)
	item1 = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name='instance_reserve1',
	)
	item2 = models.ForeignKey(
		Item,
		on_delete=models.CASCADE,
		blank=True,
		null=True,
		related_name='instance_reserve2',
	)
	objects = InstanceReserveManager()

	def __str__(self):
		return '{} ({})'.format(self.character, self.instance)

	class Meta:
		ordering = ['character', 'instance']
		unique_together = ['character', 'instance']
