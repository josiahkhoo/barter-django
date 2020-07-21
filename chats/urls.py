from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'chats'
urlpatterns = [
    url(r'^api/chats/(?P<pk>[0-9]+)$', ChatView.as_view()),
    url(r'^api/chats/(?P<pk>[0-9]+)/message/$', ChatMessageView.as_view()),
    url(r'^api/chats/(?P<pk>[0-9]+)/seen/$', ChatSeenView.as_view()),
]
