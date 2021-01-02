from django.contrib import admin

from .models import *

admin.site.register(Character)
admin.site.register(Zone)
admin.site.register(Boss)
admin.site.register(Raid)
admin.site.register(Instance)
admin.site.register(Item)
admin.site.register(Loot, LootAdmin)
admin.site.register(Member)
admin.site.register(Alt)

class NoteAdmin(admin.ModelAdmin):
    model = Note
    list_display = ('character', 'last_updated')
admin.site.register(Note, NoteAdmin)

admin.site.register(Question)
admin.site.register(Reserve)
admin.site.register(InstanceReserve)
