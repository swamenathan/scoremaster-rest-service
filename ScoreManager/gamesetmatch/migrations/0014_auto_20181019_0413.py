# Generated by Django 2.0.7 on 2018-10-19 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamesetmatch', '0013_auto_20181018_0332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='team_name',
            field=models.CharField(default='Default Team', max_length=64),
        ),
    ]
