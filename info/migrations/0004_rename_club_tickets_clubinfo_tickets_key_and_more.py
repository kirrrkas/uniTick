# Generated by Django 4.1.7 on 2023-05-25 17:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('info', '0003_article_time_create'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clubinfo',
            old_name='club_tickets',
            new_name='tickets_key',
        ),
        migrations.RenameField(
            model_name='tournamentinfo',
            old_name='tournament_tickets',
            new_name='tickets_key',
        ),
    ]
