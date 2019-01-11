from django.db import models
from django.contrib.auth.models import User
from datetime import *
import uuid


# Create your models here.
class PlayerProfile(models.Model):
    DIV_1 = 'DIV_1'
    DIV_2 = 'DIV_2'
    DIV_3 = 'DIV_3'
    DIVISION_CHOICES = (
        (DIV_1, 'Division 1'),
        (DIV_2, 'Division 2'),
        (DIV_3, 'Division 3')
    )
    player = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name='user')
    division = models.CharField(max_length=16, choices=DIVISION_CHOICES, default=DIV_3)
    seeding_points = models.CharField(max_length=3, blank=True, default='')
    rr_points = models.CharField(max_length=2, blank=True, default='')
    date_joined = models.DateTimeField(auto_now=True)


class Team(models.Model):
    team_name = models.CharField(max_length=64, blank=False, default='')
    main_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='main_player', blank=False, default='', null=False)
    partner_player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partner_player', blank=True, default=None, null=True)


class Tournament(models.Model):
    SINGLES = 'ST'
    DOUBLES = 'DT'
    MIXED_DOUBLES = 'MT'
    TOUR_TYPE = (
        (SINGLES, 'Singles Tournament'),
        (DOUBLES, 'Doubles Tournament'),
        (MIXED_DOUBLES, 'Mixed Doubles Tournament'),
    )
    tour_name = models.CharField(max_length=64, blank=True, default='')
    tour_type = models.CharField(max_length=2, choices=TOUR_TYPE, default=SINGLES)
    tour_start_date = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)
    tour_end_date = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)


class Match(models.Model):
    ROUND_ROBIN = 'RR'
    SEEDING = 'SR'
    KNOCKOUT = 'KR'
    MATCH_TYPE_CHOICES = (
        (ROUND_ROBIN, 'Round Robin'),
        (SEEDING, 'Seeding'),
        (KNOCKOUT, 'Knockout')
    )
    match_uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    match_type = models.CharField(max_length=2, choices=MATCH_TYPE_CHOICES, default=SEEDING)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default='')
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team1', default='')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team2', default='')


class Score(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_score', default='')
    team1_set1 = models.CharField(max_length=2, blank=True, default='')
    team2_set1 = models.CharField(max_length=2, blank=True, default='')
    team1_set2 = models.CharField(max_length=2, blank=True, default='')
    team2_set2 = models.CharField(max_length=2, blank=True, default='')
    team1_set3 = models.CharField(max_length=2, blank=True, default='')
    team2_set3 = models.CharField(max_length=2, blank=True, default='')
