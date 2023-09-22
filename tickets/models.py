# from django.contrib.auth.base_user import AbstractBaseUser
# from django.contrib.auth.models import PermissionsMixin
import unidecode
from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

tz = timezone.get_default_timezone()


class FanCard(models.Model):
    full_name = models.CharField(max_length=150, verbose_name=_("Полное имя"))
    is_active = models.BooleanField(default=True, verbose_name=_("Активность"))

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Карта болельщика'
        verbose_name_plural = 'Карты болельщика'
        ordering = ['id']


class Club(models.Model):
    name = models.CharField(max_length=70, verbose_name=_("Название клуба"))
    slug = models.SlugField(max_length=15, unique=True, db_index=True, verbose_name="URL")
    city = models.CharField(max_length=100, verbose_name=_("Город"))
    logo = models.ImageField(upload_to='clubs/', null=True, blank=True, verbose_name=_("Логотип"))
    stadiums = models.ManyToManyField('Stadium', blank=True, verbose_name=_("Стадионы"))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('info:club_info', kwargs={'club_slug': self.slug})

    class Meta:
        verbose_name = _('Футбольный клуб')
        verbose_name_plural = _('Футбольные клубы')
        ordering = ['name']


class Stadium(models.Model):
    name = models.CharField(max_length=100, verbose_name=_("Название стадиона"))
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL")
    city = models.CharField(max_length=100, verbose_name=_("Город"))
    places = models.FileField(upload_to='stadiums', blank=False, null=True,
                              verbose_name=_("JSON-файл для генерации мест"),
                              validators=[FileExtensionValidator(allowed_extensions=["json"])])

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('tickets:stadium', kwargs={'stadium_slug': self.slug})

    class Meta:
        verbose_name = _('Стадион')
        verbose_name_plural = _('Стадионы')
        ordering = ['city']


class Sector(models.Model):
    sec_stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE, verbose_name=_("Стадион"))
    name = models.CharField(max_length=100, verbose_name=_("Название сектора"))
    slug = models.SlugField(max_length=100, unique=True, db_index=True, verbose_name="URL", allow_unicode=True)

    # class Side(models.TextChoices):
    #     TOP_LEFT = 'TOP_LEFT', _('Сверху слева')
    #     TOP = 'TOP', _('Сверху')
    #     TOP_RIGHT = 'TOP_RIGHT', _('Сверху справа')
    #     RIGHT = 'RIGHT', _('Справа')
    #     BOTTOM_RIGHT = 'BOTTOM_RIGHT', _('Снизу справа')
    #     BOTTOM = 'BOTTOM', _('Снизу')
    #     BOTTOM_LEFT = 'BOTTOM_LEFT', _('Снизу слева')
    #     LEFT = 'LEFT', _('Слева')

    side = models.CharField(max_length=20, verbose_name=_("Сторона на схеме"), db_index=True)  # choices=Side.choices,

    def __str__(self):
        return f"сектор {self.name}"

    # def save(self, *args, **kwargs):
    #     if not self.pk:
    #         # Newly created object, so set slug
    #         self.s = slugify(f"{self.sec_stadium} {self.name}")
    #
    #     super(Sector, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(f"{self.sec_stadium.slug} {self.name}")

        super(Sector, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('sector', kwargs={'sector_slug': self.slug})

    class Meta:
        verbose_name = _('Сектор')
        verbose_name_plural = _('Секторы')
        ordering = ['sec_stadium']
        unique_together = ('sec_stadium', 'name',)


class Place(models.Model):
    p_sector = models.ForeignKey('Sector', on_delete=models.CASCADE, verbose_name=_("Сектор"))
    row = models.PositiveIntegerField()
    place = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.p_sector} ряд {self.row} место {self.place}"

    class Meta:
        verbose_name = _('Место')
        verbose_name_plural = _('Места')
        ordering = ['p_sector']


class Tournament(models.Model):
    name = models.CharField(max_length=70, verbose_name=_("Название турнира"))
    slug = models.SlugField(max_length=15, unique=True, db_index=True, verbose_name="URL")
    logo = models.ImageField(upload_to='tournaments/', null=True, blank=True, verbose_name=_("Логотип"))

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('info:tournament_info', kwargs={'tourn_slug': self.slug})

    class Meta:
        verbose_name = _('Турнир')
        verbose_name_plural = _('Турниры')
        ordering = ['name']


class Match(models.Model):
    tournament = models.ForeignKey('Tournament', on_delete=models.PROTECT, verbose_name=_("Турнир"))
    datetime_match = models.DateTimeField(verbose_name=_("Время проведения"))
    stadium = models.ForeignKey('Stadium', on_delete=models.CASCADE, verbose_name=_("Стадион"))
    clubs = models.ManyToManyField('Club', through='MatchClub')
    # home_club = models.ForeignKey('Club', related_name="match_home",
    #                               on_delete=models.CASCADE, verbose_name=_("Домашний клуб"))
    # guest_club = models.ForeignKey('Club', related_name="match_guest",
    #                                on_delete=models.CASCADE, verbose_name=_("Гостевой клуб"))
    slug = models.SlugField(max_length=50, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return f"{self.clubs.get(matchclub__is_home=True)} - {self.clubs.get(matchclub__is_home=False)}"
        # f"{self.datetime_match.astimezone(tz).strftime('%d.%m.%Y %H:%M')}, {self.stadium}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(
                f"{self.datetime_match.astimezone(tz).strftime('%d/%m/%Y')} {self.stadium.slug} {self.tournament.slug}"
            )
            # f"{self.clubs.get(matchclub__is_home=True)} - {self.clubs.get(matchclub__is_home=False)}, "
        super(Match, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('tickets:stadium', kwargs={'match_slug': self.slug})

    class Meta:
        verbose_name = _('Матч')
        verbose_name_plural = _('Матчи')
        ordering = ['datetime_match']


class MatchClub(models.Model):
    match = models.ForeignKey('Match', on_delete=models.CASCADE, verbose_name=_("Матч"))
    club = models.ForeignKey('Club', on_delete=models.CASCADE, verbose_name=_("Клуб"))
    is_home = models.BooleanField(verbose_name=_("Домашний матч"), default=False)

    class Meta:
        verbose_name = _('Клуб, участвующий в матче')
        verbose_name_plural = _('Клубы, участвующие в матче')
        # unique_together = ('match', 'is_home',)
        constraints = [
            UniqueConstraint(
                fields=['match', 'is_home'],
                name='unique_match_home',
                condition=Q(is_home=True)
            )
        ]


class Ticket(models.Model):
    on_sale = models.BooleanField(default=True, verbose_name=_("В продаже"))
    price = models.PositiveIntegerField(verbose_name=_("Цена билета"))
    t_place = models.ForeignKey('Place', on_delete=models.CASCADE, verbose_name=_("Место"))
    t_match = models.ForeignKey('Match', on_delete=models.CASCADE, verbose_name=_("Матч"))
    owner = models.ForeignKey('userapp.User', on_delete=models.PROTECT, null=True, verbose_name=_("Владелец билета"))

    def __str__(self):
        return f"{self.t_match}, {self.t_place}"

    class Meta:
        verbose_name = _('Билет')
        verbose_name_plural = _('Билеты')
        ordering = ['t_match__datetime_match', 'on_sale']
        unique_together = ('t_place', 't_match',)
        constraints = [
            models.CheckConstraint(
                check=(
                        (
                                Q(on_sale__exact=True) &
                                Q(owner__isnull=True)
                        )
                        | (
                                Q(on_sale__exact=False)
                        )
                ),
                name='on_sale_only_without_owner',
            )
        ]
