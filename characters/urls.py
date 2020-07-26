from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'characters'
urlpatterns = [
    url(r'^api/characters/(?P<pk>[0-9]+)$', CharacterView.as_view()),
    url(r'^api/characters/$', CharacterView.as_view()),
    url(r'^api/characters/achievements/(?P<pk>[0-9]+)$',
        CharacterAchievementView.as_view()),
]
