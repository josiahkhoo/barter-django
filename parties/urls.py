from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'parties'
urlpatterns = [
    url(r'^api/parties/(?P<pk>[0-9]+)$', PartyView.as_view()),
    url(r'^api/parties/$', PartyView.as_view()),
    url(r'^api/parties/join/(?P<access_code>[a-zA-Z0-9_]+)$',
        PartyJoinView.as_view()),
    url(r'^api/parties/leave/(?P<pk>[0-9]+)$', PartyLeaveView.as_view()),
    url(r'^api/parties/kick/(?P<pk>[0-9]+)$', PartyKickView.as_view()),
]
