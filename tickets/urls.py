from django.urls import path
from .views import *

app_name = 'tickets'
urlpatterns = [
    path('', MatchList.as_view(), name='home'),
    path('add_match/', AddMatch.as_view(), name='add_match'),
    path('add_tickets/<slug:match>/', add_tickets, name='add_tickets'),
    path('<slug:match_slug>/stadium/', ShowMatch.as_view(), name='stadium'),
    path('<slug:match_slug>/stadium/<slug:sector_slug>', show_sector, name='sector'),
]
