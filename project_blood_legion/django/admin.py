from django.contrib import admin

from .models import *

admin.site.register(Character)
admin.site.register(Zone)
admin.site.register(Boss)
admin.site.register(Raid)
admin.site.register(Group)
admin.site.register(Item)
admin.site.register(Loot, LootAdmin)
