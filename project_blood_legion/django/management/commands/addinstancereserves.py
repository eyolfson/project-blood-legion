from django.core.management.base import BaseCommand, CommandError

import collections
import datetime
import pytz

from project_blood_legion.django.models import Instance, InstanceReserve, Reserve, Zone

class Command(BaseCommand):

	def handle(self, *args, **options):
		for zone in Zone.objects.all():
			instances = Instance.objects.filter(raid__zone=zone, name='Sunday').order_by('-id')
			if instances.count() == 0:
				continue
			instance = instances[0]
			for reserve in Reserve.objects.filter(zone=zone):
				instance_reserve, _ = InstanceReserve.objects.get_or_create(
					character=reserve.character,
					instance=instance
				)
				instance_reserve.item1 = reserve.item1
				instance_reserve.item2 = reserve.item2
				instance_reserve.save()
				instance.characters.add(reserve.character)
			self.stdout.write(self.style.SUCCESS('Added instance reserves for "%s"' % instance))
