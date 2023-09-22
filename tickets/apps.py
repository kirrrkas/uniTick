from django.apps import AppConfig
from django.contrib.admin.apps import AdminConfig
from django.db.models.signals import post_save, m2m_changed

import userapp
# from userapp.models import User


class TicketsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tickets'
    verbose_name = 'Билеты'

    def ready(self):
        from tickets.signals import created_places  # , tickets_buying , created_tickets
        stadium = self.get_model('Stadium')
        post_save.connect(created_places, sender=stadium)
        # match = self.get_model('Match')
        # post_save.connect(created_tickets, sender=match)
        # user = userapp.get_model('User')
        # m2m_changed.connect(tickets_buying, sender=user.tickets.through)

# class MyAdminConfig(AdminConfig):
#     default_site = 'tickets.admin.MyAdminSite'
