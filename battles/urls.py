from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'battles'
urlpatterns = [
    url(r'^api/battles/(?P<pk>[0-9]+)$', BattleView.as_view()),
    url(r'^api/battles/$', BattleView.as_view()),
    url(r'^api/battles/(?P<pk>[0-9]+)/complete/$',
        BattleCompleteView.as_view()),
    url(r'^api/battles/(?P<pk>[0-9]+)/forfeit/$', BattleForfeitView.as_view()),
]
