# Generated by Django 4.1.7 on 2023-05-15 19:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Владелец билета'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='t_match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.match', verbose_name='Матч'),
        ),
        migrations.AddField(
            model_name='ticket',
            name='t_place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.place', verbose_name='Место'),
        ),
        migrations.AddField(
            model_name='sector',
            name='sec_stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.stadium', verbose_name='Стадион'),
        ),
        migrations.AddField(
            model_name='place',
            name='p_sector',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.sector', verbose_name='Сектор'),
        ),
        migrations.AddField(
            model_name='matchclub',
            name='club',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.club', verbose_name='Клуб'),
        ),
        migrations.AddField(
            model_name='matchclub',
            name='match',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.match', verbose_name='Матч'),
        ),
        migrations.AddField(
            model_name='match',
            name='clubs',
            field=models.ManyToManyField(through='tickets.MatchClub', to='tickets.club'),
        ),
        migrations.AddField(
            model_name='match',
            name='stadium',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tickets.stadium', verbose_name='Стадион'),
        ),
        migrations.AddField(
            model_name='match',
            name='tournament',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='tickets.tournament', verbose_name='Турнир'),
        ),
        migrations.AddField(
            model_name='club',
            name='stadiums',
            field=models.ManyToManyField(blank=True, to='tickets.stadium', verbose_name='Стадионы'),
        ),
        migrations.AddConstraint(
            model_name='ticket',
            constraint=models.CheckConstraint(check=models.Q(models.Q(('on_sale__exact', True), ('owner__isnull', True)), ('on_sale__exact', False), _connector='OR'), name='on_sale_only_without_owner'),
        ),
        migrations.AlterUniqueTogether(
            name='ticket',
            unique_together={('t_place', 't_match')},
        ),
        migrations.AlterUniqueTogether(
            name='sector',
            unique_together={('sec_stadium', 'name')},
        ),
        migrations.AddConstraint(
            model_name='matchclub',
            constraint=models.UniqueConstraint(condition=models.Q(('is_home', True)), fields=('match', 'is_home'), name='unique_match_home'),
        ),
    ]