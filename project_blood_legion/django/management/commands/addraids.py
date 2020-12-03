from django.core.management.base import BaseCommand, CommandError

import collections
import datetime
import pytz

from project_blood_legion.django.models import Raid, Zone

class Command(BaseCommand):

	def handle(self, *args, **options):
		Entry = collections.namedtuple('Entry', 'next_reset zone_id reset_frequency raid')
		entries = []
		eastern_tz = pytz.timezone('US/Eastern')
		release = datetime.datetime(2019, 8, 26, 22, 0, tzinfo=pytz.utc)

		molten_core_zone = Zone.objects.get(name='Molten Core')
		molten_core_first_reset = datetime.datetime(2019, 9, 3, 11, 0, 0)
		molten_core, _ = Raid.objects.get_or_create(zone=molten_core_zone, reset=1, defaults={
			'start': release,
			'end': eastern_tz.localize(molten_core_first_reset)
		})
		entries.append(Entry(
			next_reset=molten_core_first_reset,
			zone_id=molten_core_zone.id,
			reset_frequency=7,
			raid=molten_core
		))

		onyxia_zone = Zone.objects.get(name="Onyxia's Lair")
		onyxia_first_reset = datetime.datetime(2019, 9, 2, 11, 0, 0)
		onyxia, _ = Raid.objects.get_or_create(zone=onyxia_zone, reset=1, defaults={
			'start': release,
			'end': eastern_tz.localize(onyxia_first_reset)
		})
		entries.append(Entry(
			next_reset=onyxia_first_reset,
			zone_id=onyxia_zone.id,
			reset_frequency=5,
			raid=onyxia
		))

		bwl_zone = Zone.objects.get(name="Blackwing Lair")
		bwl_release = datetime.datetime(2020, 2, 12, 18, 0, 0)
		bwl_first_reset = datetime.datetime(2020, 2, 18, 11, 0, 0)
		bwl, _ = Raid.objects.get_or_create(zone=bwl_zone, reset=1, defaults={
			'start': eastern_tz.localize(bwl_release),
			'end': eastern_tz.localize(bwl_first_reset)
		})
		entries.append(Entry(
			next_reset=bwl_first_reset,
			zone_id=bwl_zone.id,
			reset_frequency=7,
			raid=bwl
		))

		aq_zone = Zone.objects.get(name="Temple of Ahn'Qiraj")
		aq_release = datetime.datetime(2020, 8, 4, 12, 0, 0)
		aq_first_reset = datetime.datetime(2020, 8, 11, 12, 0, 0)
		aq, _ = Raid.objects.get_or_create(zone=aq_zone, reset=1, defaults={
			'start': eastern_tz.localize(aq_release),
			'end': eastern_tz.localize(aq_first_reset)
		})
		entries.append(Entry(
			next_reset=aq_first_reset,
			zone_id=aq_zone.id,
			reset_frequency=7,
			raid=aq
		))

		naxx_zone = Zone.objects.get(name="Naxxramas")
		naxx_release = datetime.datetime(2020, 12, 3, 17, 0, 0)
		naxx_first_reset = datetime.datetime(2020, 12, 8, 11, 0, 0)
		naxx, _ = Raid.objects.get_or_create(zone=naxx_zone, reset=1, defaults={
			'start': eastern_tz.localize(naxx_release),
			'end': eastern_tz.localize(naxx_first_reset)
		})
		entries.append(Entry(
			next_reset=naxx_first_reset,
			zone_id=naxx_zone.id,
			reset_frequency=7,
			raid=naxx
		))

		until = datetime.datetime.now() + datetime.timedelta(days=14)
		while True:
			entries = sorted(entries)
			entry = entries.pop(0)
			if entry.next_reset > until:
				break
			start = entry.next_reset
			end = entry.next_reset + datetime.timedelta(days=entry.reset_frequency)
			raid, created = Raid.objects.get_or_create(zone=entry.raid.zone,
			                                           reset=entry.raid.reset + 1,
			                                           defaults={
				'start': eastern_tz.localize(start),
				'end': eastern_tz.localize(end)
			})
			if created:
				self.stdout.write(self.style.SUCCESS('Added raid "%s"' % raid))
			entries.append(Entry(
				next_reset=end,
				zone_id=entry.zone_id,
				reset_frequency=entry.reset_frequency,
				raid=raid
			))
