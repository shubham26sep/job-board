from django.contrib import admin

from jobs.apps.users.models import User, Location, Skill

admin.site.register(User)
admin.site.register(Location)
admin.site.register(Skill)
