from django.contrib import admin
from teams.models import Team, TeamFilter

admin.site.register(Team)
admin.site.register(TeamFilter)
