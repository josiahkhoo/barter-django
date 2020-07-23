from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'chats'
urlpatterns = [
    url(r'^api/chats/(?P<pk>[0-9]+)$', ChatView.as_view()),
    url(r'^api/chats/(?P<pk>[0-9]+)/message/$', ChatMessageView.as_view()),
    url(r'^api/chats/(?P<pk>[0-9]+)/seen/$', ChatSeenView.as_view()),
    url(r'^api/chats/conversation/(?P<pk>[0-9]+)/message/$',
        UserMessageView.as_view()),
    url(r'^api/chats/user/(?P<pk>[0-9]+)$',
        UserConversationView.as_view()),
]
