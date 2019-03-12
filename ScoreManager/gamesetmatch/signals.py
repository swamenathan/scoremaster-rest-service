from django.db.models.signals import *
from .models import *
from django.dispatch import receiver


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
    if created:
        print('Increment Team score', instance.match_type)

        if instance.winner == Match.TEAM_1:
            team = Team.objects.get(pk=instance.team_1.pk)
            team.seeding_points += 1
            team.save()
        elif instance.winner == Match.TEAM_2:
            team = Team.objects.get(pk=instance.team_2.pk)
            team.seeding_points += 1
            team.save()
        elif instance.winner == Match.DRAW:
            team_1 = Team.objects.get(pk=instance.team_1.pk)
            team_2 = Team.objects.get(pk=instance.team_2.pk)
            team_1.seeding_points += 0.5
            team_2.seeding_points += 0.5
            team_1.save()
            team_2.save()
        else:
            print('Nothing needs to be done')

    if update_fields is not None and any(['winner' in fields for fields in update_fields]):
        print('Update scores', instance.previous_winner)
        if instance.previous_winner == Match.TEAM_1:
            team = Team.objects.get(pk=instance.team_1.pk)
            team.seeding_points -= 1
            team.save()
        elif instance.previous_winner == Match.TEAM_2:
            team = Team.objects.get(pk=instance.team_2.pk)
            team.seeding_points -= 1
            team.save()
        elif instance.previous_winner == Match.DRAW:
            team_1 = Team.objects.get(pk=instance.team_1.pk)
            team_2 = Team.objects.get(pk=instance.team_2.pk)
            team_1.seeding_points -= 0.5
            team_2.seeding_points -= 0.5
            team_1.save()
            team_2.save()




