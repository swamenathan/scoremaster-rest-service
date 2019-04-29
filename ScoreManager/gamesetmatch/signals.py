from django.db.models.signals import *
from .models import *
from django.dispatch import receiver
from django.core.exceptions import *


@receiver(post_save, sender=Match)
def on_save_match(sender, instance, created, raw, using, update_fields, **kwargs):
    """
    Perform administrative functions after a reservation was created or updated.
    :param sender: The model class.
    :param instance: The actual instance being saved.
    :param created: A boolean; True if a new record was created.
    :param raw: A boolean; True if the model is saved exactly as presented (i.e. when loading a fixture).
    :param using: The database alias being used.
    :param update_fields: The set of fields to update as passed to Model.save(), or None if update_fields wasn’t passed to save().
    :return:
    """
    team_1 = Team.objects.get(pk=instance.team_1.pk)
    team_2 = Team.objects.get(pk=instance.team_2.pk)

    if instance.match_type == Match.SEEDING:
        points = 1
    elif instance.match_type == Match.ROUND_ROBIN:
        points = 1
    elif instance.match_type == Match.KNOCKOUT:
        points = 1

    def add_points():
        if instance.winner == Match.TEAM_1:
            team_1.seeding_points += points
            team_1.save()
        elif instance.winner == Match.TEAM_2:
            team_2.seeding_points += points
            team_2.save()
        elif instance.winner == Match.DRAW:
            team_1.seeding_points += points / 2
            team_2.seeding_points += points / 2
            team_1.save()
            team_2.save()
        else:
            print('Nothing needs to be done')

    def negate_points():
        if instance.previous_winner == Match.TEAM_1:
            team_1.seeding_points -= points
            team_1.save()
        elif instance.previous_winner == Match.TEAM_2:
            team_2.seeding_points -= points
            team_2.save()
        elif instance.previous_winner == Match.DRAW:
            # Potential bug here if previous match is of different Type.
            team_1.seeding_points -= points / 2
            team_2.seeding_points -= points / 2
            team_1.save()
            team_2.save()

    def add_set():
        team_1.rr_points += float(instance.team1_set1)
        team_2.rr_points += float(instance.team2_set1)
        team_1.save()
        team_2.save()

        try:
            previous_score = PreviousScore.objects.get(match_id=instance.match_uuid)
            previous_score.team1_set1 = instance.team1_set1
            previous_score.team2_set1 = instance.team2_set1
            previous_score.save()
        except ObjectDoesNotExist:
            previous_score = PreviousScore.objects.create()
            previous_score.match_id = instance.match_uuid
            previous_score.team1_set1 = instance.team1_set1
            previous_score.team2_set1 = instance.team2_set1
            previous_score.save()


    def negate_set():
        previous_score = PreviousScore.objects.get(match_id=instance.match_uuid)
        team_1.rr_points -= float(previous_score.team1_set1)
        team_2.rr_points -= float(previous_score.team2_set1)
        team_1.save()
        team_2.save()

    if created:
        if instance.match_type == Match.ROUND_ROBIN:
            add_set()


    if update_fields is not None and any(['winner' in fields for fields in update_fields]):
        if instance.match_type == Match.ROUND_ROBIN:
            negate_set()
            add_set()


@receiver(post_delete, sender=Match)
def on_delete_match(sender, instance, using, **kwargs):

    try:
        previous_score = PreviousScore.objects.get(match_id=instance.match_uuid)
    except ObjectDoesNotExist:
        previous_score = None

    if previous_score is not None:
        team_1 = Team.objects.get(pk=instance.team_1.pk)
        team_2 = Team.objects.get(pk=instance.team_2.pk)

        team_1.rr_points -= float(previous_score.team1_set1)
        team_2.rr_points -= float(previous_score.team2_set1)
        team_1.save()
        team_2.save()

        previous_score.delete()