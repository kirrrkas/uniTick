from django.urls import path
from .views import *

app_name = 'info'
urlpatterns = [
    path('', ArticleList.as_view(), name='home'),
    path('article/<slug:article_slug>', ShowArticle.as_view(), name='article'),
    path('clubs/<slug:club_slug>', ShowClubInfo.as_view(), name='club_info'),
    path('tournaments/<slug:tournament_slug>', ShowTournamentInfo.as_view(), name='tournament_info'),
]
