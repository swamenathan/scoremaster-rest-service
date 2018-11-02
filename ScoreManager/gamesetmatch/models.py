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
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name='user')
    division = models.CharField(max_length=16, choices=DIVISION_CHOICES, default=DIV_3)
    seeding_points = models.CharField(max_length=3, blank=True, default='')
    rr_points = models.CharField(max_length=2, blank=True, default='')
    date_joined = models.DateTimeField(auto_now=True)


class Team(models.Model):
    team_name = models.CharField(max_length=64, blank=False, default='Default Team')
    player_1 = models.CharField(max_length=3, blank=False, default=1)
    player_2 = models.CharField(max_length=3, blank=True, default='')
    player_3 = models.CharField(max_length=3, blank=True, default='')


class Match(models.Model):
    ROUND_ROBIN = 'RR'
    SEEDING = 'SR'
    KNOCKOUT = 'KR'
    MATCH_TYPE_CHOICES = (
        (ROUND_ROBIN, 'Round Robin'),
        (SEEDING, 'Seeding'),
        (KNOCKOUT, 'Knockout')
    )
    match_uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_1')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='team_2')
    match_type = models.CharField(max_length=2, choices=MATCH_TYPE_CHOICES, default=SEEDING)


class Score(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match_score', default='')
    team1_set1 = models.CharField(max_length=2, blank=True, default='')
    team2_set1 = models.CharField(max_length=2, blank=True, default='')
    team1_set2 = models.CharField(max_length=2, blank=True, default='')
    team2_set2 = models.CharField(max_length=2, blank=True, default='')
    team1_set3 = models.CharField(max_length=2, blank=True, default='')
    team2_set3 = models.CharField(max_length=2, blank=True, default='')


class Tournament(models.Model):
    SINGLES = 'ST'
    DOUBLES = 'DT'
    MIXED_DOUBLES = 'MT'
    TOUR_TYPE = (
        (SINGLES, 'Singles Tournament'),
        (DOUBLES, 'Doubles Tournament'),
        (MIXED_DOUBLES, 'Mixed Doubles Tournament'),
    )
    tour_year = models.DateField(auto_now=False, auto_now_add=False)
    tour_type = models.CharField(max_length=2, choices=TOUR_TYPE, default=SINGLES)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='match')






