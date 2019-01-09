from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources


class PlayerProfileResource(resources.ModelResource):
    class Meta:
        model = PlayerProfile
        fields = ('player__first_name','division', )


class PlayerProfileAdmin(ImportExportActionModelAdmin):
    resource_class = PlayerProfileResource


# Register your models here.
admin.site.register(PlayerProfile, PlayerProfileAdmin)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(Tournament)