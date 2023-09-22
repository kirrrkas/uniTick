from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Group
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _
from tickets.models import FanCard
from userapp.managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name=_("Эл. почта"))
    phone_number = models.CharField(max_length=16, unique=True, verbose_name=_("Номер телефона"))
    last_name = models.CharField(max_length=50, verbose_name=_("Фамилия"))
    first_name = models.CharField(max_length=50, verbose_name=_("Имя"))
    middle_name = models.CharField(max_length=50, null=True, blank=True, verbose_name=_("Отчество"))
    is_verified = models.BooleanField(default=False, verbose_name=_("Подтвержденный аккаунт"))
    is_staff = models.BooleanField(default=False, verbose_name=_("Работник"))

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'last_name', 'first_name', 'middle_name']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        # constraints = [
        #     # For fan_card == null only
        #     models.UniqueConstraint(fields=['name'], name='unique__when__fan_card__null',
        #                             condition=Q(fan_card__isnull=True)),
        #     # For fan_card != null only
        #     models.UniqueConstraint(fields=['name', 'fan_card'], name='unique__when__fan_card__not_null')
        # ]

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.last_name} {self.first_name} {self.middle_name}"
        return full_name.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email], **kwargs)

