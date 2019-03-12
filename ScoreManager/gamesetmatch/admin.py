from django.contrib import admin
from .models import *
from import_export.admin import ImportExportActionModelAdmin, ImportExportModelAdmin
from import_export import resources
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _


class PlayerProfileAdmin(admin.ModelAdmin):

    list_display = ('player', 'phone')


class TeamResource(resources.ModelResource):

    class Meta:
        model = Team
        fields = ('team_name', 'main_player__first_name', 'partner_player__first_name', 'seeding_points', 'rr_points')



class TeamAdmin(ImportExportModelAdmin):

    resource_class = TeamResource

    list_display = ('team_name', 'main_player', 'partner_player', 'seeding_points', 'rr_points')


class MatchResource(resources.ModelResource):

    class Meta:
        model = Match
        fields = ('tournament__tour_name', 'match_date', 'match_type', 'team_1__team_name', 'team_2__team_name', 'team1_set1', 'team2_set1', 'team1_set2', 'team2_set2', 'team1_set3', 'team2_set3')


class TournamentAdmin(admin.ModelAdmin):

    list_display = ('tour_name', 'tour_type', 'tour_start_date', 'tour_end_date')


class MatchAdmin(ImportExportModelAdmin):

    resource_class = MatchResource

    list_display = ('match_uuid', 'match_date', 'team_1', 'team_2', 'match_type')
    ordering = ('match_date', )
    readonly_fields = ('winner', )


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
admin.site.register(Team, TeamAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Tournament, TournamentAdmin)
admin.site.register(TennisUser, TennisUserAdmin)