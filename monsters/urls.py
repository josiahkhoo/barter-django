from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

from .views import *

app_name = 'monsters'
urlpatterns = [
    url(r'^api/monsters/(?P<pk>[0-9]+)$', MonsterView.as_view()),
    url(r'^api/monsters/$', MonsterView.as_view()),
]
