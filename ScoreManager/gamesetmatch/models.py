from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from datetime import *
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404



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
    player = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, related_name='user')
    division = models.CharField(max_length=16, choices=DIVISION_CHOICES, default=DIV_3)
    phone = models.CharField(max_length=10, blank=True, default='')
    date_joined = models.DateTimeField(auto_now=True)


class Team(models.Model):

    team_name = models.CharField(max_length=64, blank=True, default='')
    main_player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='main_player', blank=False, default='', null=False)
    partner_player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='partner_player', blank=True, default=None, null=True)
    seeding_points = models.FloatField(default=0)
    rr_points = models.FloatField(default=0)

    # TODO: Ordering need to be done in Front End. This is just a temporary ugly hack
    class Meta:
        ordering = ['-rr_points']

    def __str__(self):
        return self.team_name

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        # If Team name is found to be blank set a default value
        if self.team_name == '':
            if self.partner_player is not None:
                self.team_name = self.main_player.first_name + ' ' + self.partner_player.first_name + ' Team'
            else:
                self.team_name = self.main_player.first_name + ' ' + self.main_player.last_name
        super(Team, self).save()




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

    def __str__(self):
        return self.tour_name


class Match(models.Model):
    ROUND_ROBIN = 'RR'
    SEEDING = 'SR'
    KNOCKOUT = 'KR'
    QUARTER = 'QF'
    SEMI = 'SF'
    FINAL = 'FF'
    MATCH_TYPE_CHOICES = (
        (ROUND_ROBIN, 'Round Robin'),
        (SEEDING, 'Seeding'),
        (KNOCKOUT, 'Knockout'),
        (QUARTER, 'Quarter'),
        (SEMI, 'Semi'),
        (FINAL, 'Final'),
    )

    TEAM_1 = 'T1'
    TEAM_2 = 'T2'
    NONE = 'NONE'
    DRAW = 'DRAW'
    WINNER_TYPE_CHOICES = (
        (TEAM_1, 'Team 1'),
        (TEAM_2, 'Team 2'),
        (NONE, 'None'),
        (DRAW, 'Draw')
    )

    player_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='player_id', blank=True, default='', null=True)
    match_uuid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    match_type = models.CharField(max_length=2, choices=MATCH_TYPE_CHOICES, default=SEEDING)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, default='')
    team_1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team1', default='')
    team_2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='match_team2', default='')
    team1_set1 = models.CharField(max_length=3, blank=True, default='')
    team2_set1 = models.CharField(max_length=3, blank=True, default='')
    team1_set2 = models.CharField(max_length=3, blank=True, default='')
    team2_set2 = models.CharField(max_length=3, blank=True, default='')
    team1_set3 = models.CharField(max_length=3, blank=True, default='')
    team2_set3 = models.CharField(max_length=3, blank=True, default='')
    winner = models.CharField(max_length=4, choices=WINNER_TYPE_CHOICES, default=NONE)

    match_date = models.DateField(auto_now=False, auto_now_add=False, default=None, null=True)

    
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        update_fields = []
        t1_total = self.team1_set1 + self.team1_set2 + self.team1_set3
        t2_total = self.team2_set1 + self.team2_set2 + self.team2_set3

        if t1_total > t2_total:
            self.winner = Match.TEAM_1
        elif t2_total > t1_total:
            self.winner = Match.TEAM_2
        else:
            self.winner = Match.DRAW

        try:
            match_in_db = Match.objects.get(pk=self.match_uuid)
        except Match.DoesNotExist:
            match_in_db = None

        if match_in_db is not None:
            if match_in_db.team1_set1 != self.team1_set1 or match_in_db.team2_set1 != self.team2_set1:
                update_fields.append('winner')
                super(Match, self).save(update_fields=update_fields)

        super(Match, self).save()


class PreviousScore(models.Model):

    match_id = models.UUIDField(default=uuid.uuid4, editable=False)
    team1_set1 = models.CharField(max_length=2, blank=True, default='')
    team2_set1 = models.CharField(max_length=2, blank=True, default='')


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class TennisUser(AbstractUser):

    username = None
    email = models.EmailField('email address', unique=True, max_length = 255)
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_(
            'Designates whether this user should be treated as verified. '
            'Unselect this if not a valid user.'
        ),
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()
