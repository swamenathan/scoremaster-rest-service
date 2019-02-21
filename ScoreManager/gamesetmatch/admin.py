from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class PlayerProfileResource(resources.ModelResource):
    class Meta:
        model = PlayerProfile
        fields = ('player__first_name','division', )


class PlayerProfileAdmin(ImportExportActionModelAdmin):
    resource_class = PlayerProfileResource


class TennisUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_verified', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )

    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active', 'is_verified')

    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)

# Register your models here.
admin.site.register(PlayerProfile, PlayerProfileAdmin)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(Tournament)
admin.site.register(TennisUser, TennisUserAdmin)