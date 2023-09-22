from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class ClubInfo(models.Model):
    tickets_key = models.OneToOneField('tickets.Club', on_delete=models.CASCADE,
                                        verbose_name=_("Клуб"), unique=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Описание клуба"))

    def __str__(self):
        return self.tickets_key.name

    def get_absolute_url(self):
        return reverse('club', kwargs={'club_slug': self.tickets_key.slug})

    class Meta:
        verbose_name = 'Клуб'
        verbose_name_plural = 'Клубы'
        ordering = ['pk']


class TournamentInfo(models.Model):
    tickets_key = models.OneToOneField('tickets.Tournament', on_delete=models.CASCADE,
                                              verbose_name=_("Турнир"), unique=True)
    description = models.TextField(null=True, blank=True, verbose_name=_("Описание турнира"))

    def __str__(self):
        return self.tickets_key.name

    def get_absolute_url(self):
        return reverse('tournament', kwargs={'tournament_slug': self.tickets_key.slug})

    class Meta:
        verbose_name = 'Турнир'
        verbose_name_plural = 'Турниры'
        ordering = ['pk']


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    content = models.TextField(verbose_name=_("Текст статьи"))
    is_published = models.BooleanField(default=True, verbose_name="Публикация")
    clubs = models.ManyToManyField('ClubInfo', blank=True, verbose_name=_("Клубы, относящиеся к статье"))
    tournaments = models.ManyToManyField('TournamentInfo', blank=True, verbose_name=_("Турниры, относящиеся к статье"))
    image = models.ImageField(upload_to='articles/', null=True, blank=True, verbose_name=_("Изображение"))
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_slug': self.slug})

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['pk']
